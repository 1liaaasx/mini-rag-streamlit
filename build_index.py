"""Construit une fois l'index à partir de l'archive HTML officielle Python 3.13."""

import argparse
import gzip
import hashlib
import json
import re
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

import faiss
import numpy as np
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer


VERSION = "3.13"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
ARCHIVE_URL = "https://docs.python.org/3.13/archives/python-3.13-docs-html.zip"
ARCHIVE_PREFIX = "python-3.13-docs-html/"
OUTPUT_DIR = Path(__file__).resolve().parent / "index"
MAX_CHARS = 1050

# Périmètre explicite et reproductible : une sélection des pages officielles,
# et non la prétention de couvrir l'intégralité de la documentation Python.
PAGES = (
    "builtins/functions.html", "builtins/stdtypes.html", "builtins/exceptions.html",
    "library/pathlib.html", "library/json.html", "library/asyncio-task.html",
    "library/asyncio-eventloop.html", "library/contextlib.html",
    "library/os.html", "library/io.html", "library/csv.html",
    "library/collections.html", "library/functools.html",
    "library/itertools.html",
    "library/logging.html", "library/typing.html", "library/re.html",
    "library/datetime.html", "library/subprocess.html",
    "library/unittest.html", "library/concurrent.futures.html",
    "library/sqlite3.html", "library/enum.html",
    "tutorial/errors.html", "tutorial/datastructures.html",
    "reference/compound_stmts.html", "reference/datamodel.html",
)


def clean_text(element):
    """Extrait du texte lisible en conservant les blocs de code."""
    for link in element.select("a.headerlink"):
        link.decompose()
    text = element.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip()


def split_text(text):
    """Découpe un extrait avec un léger chevauchement, sans couper les mots."""
    start = 0
    while start < len(text):
        end = min(start + MAX_CHARS, len(text))
        if end < len(text):
            space = text.rfind(" ", start + MAX_CHARS // 2, end)
            if space > start:
                end = space
        piece = text[start:end].strip()
        if len(piece) >= 35:
            yield piece
        if end == len(text):
            break
        start = max(start + 1, end - 100)


def module_name(path):
    name = Path(path).stem
    if path.startswith("builtins/"):
        return "builtins"
    if name == "asyncio-task" or name == "asyncio-eventloop":
        return "asyncio"
    if path.startswith("tutorial/"):
        return "tutorial"
    if path.startswith("reference/"):
        return "language reference"
    return name


def parse_page(archive, path):
    soup = BeautifulSoup(archive.read(ARCHIVE_PREFIX + path), "html.parser")
    body = soup.select_one("div.body")
    if body is None:
        raise ValueError(f"Page officielle sans contenu exploitable : {path}")
    title = soup.title.get_text(" ", strip=True).split(" — Python ")[0]
    module = module_name(path)
    base_url = f"https://docs.python.org/{VERSION}/{path}"
    records = []

    def append_chunks(section, source_url, content, api_name="", limit=5):
        for chunk in list(split_text(content))[:limit]:
            records.append({
                "language": "python", "version": VERSION,
                "module": module, "section": section, "title": title,
                "source_url": source_url, "api_name": api_name,
                "content": chunk,
            })

    # Définitions d'API : les identifiants HTML fournis par Sphinx sont les ancres.
    for definition in body.select("dl.py"):
        dt = definition.find("dt", id=True, recursive=False)
        dd = definition.find("dd", recursive=False)
        if dt is None or dd is None:
            continue
        api_name = dt["id"]
        detail = BeautifulSoup(str(dd), "html.parser")
        for nested in detail.select("dl"):
            nested.decompose()
        signature = clean_text(BeautifulSoup(str(dt), "html.parser"))
        description = clean_text(detail)
        append_chunks(api_name, f"{base_url}#{api_name}",
                      f"{api_name} — {signature}. {description}", api_name)

    # Paragraphes conceptuels : uniquement les enfants directs de chaque section.
    for section in body.select("section[id]"):
        heading = section.find(re.compile("^h[1-6]$"), recursive=False)
        if heading is None:
            continue
        section_name = clean_text(BeautifulSoup(str(heading), "html.parser"))
        direct = [str(child) for child in section.find_all(
            ["p", "pre", "ul", "ol"], recursive=False
        )]
        if not direct:
            continue
        content = clean_text(BeautifulSoup(" ".join(direct), "html.parser"))
        append_chunks(section_name, f"{base_url}#{section['id']}",
                      f"{section_name}. {content}", limit=3)
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, help="Archive HTML Python 3.13 déjà téléchargée")
    args = parser.parse_args()

    if args.archive:
        archive_path = args.archive
        temporary = None
    else:
        temporary = tempfile.TemporaryDirectory()
        archive_path = Path(temporary.name) / "python-docs.zip"
        print(f"Téléchargement depuis {ARCHIVE_URL}", flush=True)
        urllib.request.urlretrieve(ARCHIVE_URL, archive_path)

    try:
        with ZipFile(archive_path) as archive:
            records = [record for path in PAGES for record in parse_page(archive, path)]
        if not records:
            raise ValueError("Aucun passage extrait de la documentation")
        print(f"{len(records)} passages issus de {len(PAGES)} pages officielles", flush=True)

        model = SentenceTransformer(MODEL_NAME)
        vectors = model.encode(
            [item["content"] for item in records], batch_size=64,
            convert_to_numpy=True, show_progress_bar=True,
        )
        vectors = np.ascontiguousarray(vectors, dtype="float32")
        faiss.normalize_L2(vectors)
        # Quantification 8 bits : index FAISS ~4 fois plus petit, adapté à GitHub.
        index = faiss.IndexScalarQuantizer(
            vectors.shape[1], faiss.ScalarQuantizer.QT_8bit, faiss.METRIC_INNER_PRODUCT
        )
        index.train(vectors)
        index.add(vectors)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        index_path = OUTPUT_DIR / "python-3.13.faiss"
        faiss.write_index(index, str(index_path))
        metadata_path = OUTPUT_DIR / "metadata.json.gz"
        metadata_path.write_bytes(gzip.compress(
            json.dumps(records, ensure_ascii=False, separators=(",", ":")).encode("utf-8"),
            compresslevel=9, mtime=0,
        ))
        (OUTPUT_DIR / "manifest.json").write_text(json.dumps({
            "language": "python", "version": VERSION,
            "model": MODEL_NAME, "count": len(records),
            "dimensions": int(vectors.shape[1]),
            "archive_url": ARCHIVE_URL,
            "archive_sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
            "index_sha256": hashlib.sha256(index_path.read_bytes()).hexdigest(),
            "metadata_sha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
            "pages": list(PAGES),
        }, indent=2), encoding="utf-8")
        print(f"Index enregistré dans {OUTPUT_DIR}", flush=True)
    finally:
        if temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    main()

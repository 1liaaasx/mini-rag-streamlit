"""Chargement et recherche dans l'index préconstruit de documentation Python."""

import hashlib
import gzip
import json
import re
from pathlib import Path

import faiss
import numpy as np


INDEX_DIR = Path(__file__).resolve().parent / "index"
MIN_SCORE = 0.20
TOP_K = 4
API_TOKEN = re.compile(r"\b[A-Za-z_]\w*(?:\.[A-Za-z_]\w*){0,3}\b")


def load_index(directory=INDEX_DIR):
    """Lit l'index et vérifie qu'il correspond aux passages et à la version."""
    directory = Path(directory)
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    metadata_path = directory / "metadata.json.gz"
    if hashlib.sha256(metadata_path.read_bytes()).hexdigest() != manifest["metadata_sha256"]:
        raise ValueError("Les métadonnées de documentation sont incomplètes ou modifiées.")
    records = json.loads(gzip.decompress(metadata_path.read_bytes()).decode("utf-8"))
    index_path = directory / "python-3.13.faiss"
    if hashlib.sha256(index_path.read_bytes()).hexdigest() != manifest["index_sha256"]:
        raise ValueError("L'index de documentation est incomplet ou modifié.")
    index = faiss.read_index(str(index_path))
    if (manifest["language"] != "python" or manifest["version"] != "3.13"
            or len(records) != manifest["count"] or index.ntotal != len(records)
            or index.d != manifest["dimensions"]):
        raise ValueError("L'index et ses métadonnées ne correspondent pas.")
    for record in records:
        if (record.get("language") != "python" or record.get("version") != "3.13"
                or not record.get("source_url", "").startswith("https://docs.python.org/3.13/")):
            raise ValueError("Source de documentation non reconnue dans l'index.")
    api_positions = {}
    for position, record in enumerate(records):
        api = record.get("api_name", "").casefold()
        if api:
            api_positions.setdefault(api, []).append(position)
    return index, records, manifest, api_positions


def embed_query(model, question):
    vector = np.ascontiguousarray(
        model.encode([question], convert_to_numpy=True), dtype="float32"
    )
    faiss.normalize_L2(vector)
    return vector


def mentioned_apis(text, api_positions):
    """Reconnaît seulement les API effectivement présentes dans l'index."""
    found = []
    for token in API_TOKEN.findall(text):
        key = token.casefold()
        if key in api_positions and key not in found:
            found.append(key)
    # Une formulation courante vise json.load sans prononcer son nom d'API.
    # Le nom n'est ajouté que s'il existe réellement dans la documentation indexée.
    lowered = text.casefold()
    if ("json" in lowered and any(word in lowered for word in ("file", "fichier"))
            and any(word in lowered for word in ("read", "lire", "load"))
            and "json.load" in api_positions and "json.load" not in found):
        found.insert(0, "json.load")
    # Une comparaison cite souvent deux API ; conserver les noms les plus précis.
    return sorted(found, key=len, reverse=True)[:2]


def search(question, model, index, records, api_positions, top_k=TOP_K):
    vector = embed_query(model, question)
    scores, positions = index.search(vector, min(max(top_k * 5, 20), index.ntotal))
    ranked = [(int(pos), float(score)) for pos, score in zip(positions[0], scores[0])
              if pos >= 0 and score >= MIN_SCORE]

    # Si la question nomme précisément des API indexées, réserver un résultat
    # pour chacune, même si le modèle d'embeddings anglais score le français bas.
    selected = []
    for name in mentioned_apis(question, api_positions):
        candidates = api_positions[name]
        position = max(candidates, key=lambda pos: float(index.reconstruct(pos) @ vector[0]))
        if records[position]["source_url"] not in {records[p]["source_url"] for p, _ in selected}:
            selected.append((position, float(index.reconstruct(position) @ vector[0])))

    for position, score in ranked:
        if len(selected) >= top_k:
            break
        if records[position]["source_url"] not in {records[p]["source_url"] for p, _ in selected}:
            selected.append((position, score))
    return [(records[pos], score) for pos, score in selected[:top_k]]


def lookup_api(query, records, api_positions):
    """Retourne une fiche tirée des métadonnées, sans inventer de description."""
    key = query.strip().removesuffix("()").casefold()
    if key not in api_positions:
        return None
    item = records[api_positions[key][0]]
    related = []
    for record in records:
        name = record.get("api_name", "")
        if (name and name != item["api_name"] and record["module"] == item["module"]
                and name not in related):
            related.append(name)
        if len(related) == 3:
            break
    return item, related

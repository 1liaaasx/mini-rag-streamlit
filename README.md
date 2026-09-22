# DocQuery

**Developer documentation, explained.** Une application RAG pour explorer une **sélection** de 27 pages de la documentation officielle Python 3.13. Posez une question, consultez les extraits utilisés, recherchez une API précise ou interrogez votre propre PDF dans un mode secondaire.

Le projet n'indexe **pas l'intégralité** de la documentation Python. Les pages retenues couvrent notamment les fonctions et types intégrés, les exceptions, `pathlib`, `json`, `asyncio`, `contextlib`, `os`, `re`, `typing`, `datetime`, ainsi que quelques sections du tutoriel et de la référence du langage. La liste exacte est dans `build_index.py`.

## Architecture

```text
Archive HTML officielle docs.python.org/3.13
  → sections et définitions d'API avec URL d'origine
  → chunks + métadonnées (langage, version, module, section, titre, URL)
  → embeddings locaux all-MiniLM-L6-v2
  → index FAISS quantifié sur 8 bits + métadonnées compressées dans index/

Question → nouvel embedding → recherche FAISS → 4 passages au plus
         → contexte sourcé → Groq openai/gpt-oss-20b → réponse + sources
```

`build_index.py` prépare l'index **une fois**, en téléchargeant l'archive HTML de [docs.python.org](https://docs.python.org/3.13/download.html). L'application lit les fichiers déjà préparés au démarrage ; elle ne télécharge pas la documentation et ne recalcule pas ses embeddings à chaque question. Les citations `[1]`, `[2]` ne peuvent pointer que vers les passages réellement transmis au modèle. Une citation numérotée n'est toutefois pas une garantie que la phrase associée est exacte : consultez le lien officiel.

Les questions de suivi utilisent la dernière question pour lever une ambiguïté, puis lancent **une nouvelle recherche** dans FAISS. La recherche d'API est déterministe et utilise les noms/URLs des métadonnées, sans appel Groq.

## Stack

| Dépendance | Rôle |
| --- | --- |
| Streamlit | Interface et historique temporaire de la session |
| Groq | Génération via `openai/gpt-oss-20b` |
| Sentence Transformers | Embeddings locaux, sans clé OpenAI |
| FAISS CPU | Recherche vectorielle |
| Beautiful Soup | Extraction des sections de l'archive HTML officielle |
| PyPDF | Extraction du texte en mode « My Documents » |

## Installation et lancement

Utilisez Python **3.12** :

```bash
git clone https://github.com/1liaaasx/mini-rag-streamlit.git
cd mini-rag-streamlit
python -m venv .venv
# Linux/macOS : source .venv/bin/activate
# Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Les fichiers `index/python-3.13.faiss`, `index/metadata.json.gz` et `index/manifest.json` sont déjà inclus dans le dépôt. Le premier lancement télécharge le modèle d'embeddings sur la machine locale ; cela demande Internet et peut prendre un moment. Les dépendances du modèle, dont PyTorch, consomment de la mémoire.

## Clé Groq

Créez une clé sur [GroqCloud](https://console.groq.com/keys). L'application lit `st.secrets["GROQ_API_KEY"]`, puis la variable d'environnement locale :

```bash
export GROQ_API_KEY="votre-cle"       # Linux/macOS
```

```powershell
$env:GROQ_API_KEY = "votre-cle"     # Windows PowerShell
```

Vous pouvez aussi placer `GROQ_API_KEY = "votre-cle"` dans `.streamlit/secrets.toml`, exclu de Git. **Ne publiez jamais la clé.** Aucune clé OpenAI n'est nécessaire.

## Reconstruire l'index

Exécutez, seulement lorsque vous changez les pages, la méthode de découpage ou le modèle d'embeddings :

```bash
python build_index.py
```

Pour réutiliser une archive téléchargée au préalable :

```bash
python build_index.py --archive chemin/vers/python-3.13-docs-html.zip
```

Le script remplace les trois fichiers dans `index/` ensemble. Commitez-les et déployez-les ensemble. Le manifeste inclut la version, le modèle, le nombre de passages et les empreintes de l'archive et de l'index. La licence et les modalités de réutilisation de la documentation sont consultables sur [docs.python.org](https://docs.python.org/3.13/license.html).

## Déploiement Streamlit Community Cloud

1. Connectez le dépôt GitHub `1liaaasx/mini-rag-streamlit` sur [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sélectionnez `app.py` et Python 3.12.
3. Dans **Secrets**, ajoutez :

   ```toml
   GROQ_API_KEY = "votre-cle"
   ```

4. Déployez. `requirements.txt` installe les dépendances et l'application charge l'index versionné dans le dépôt.

## Fonctionnalités et limites

- **Ask Documentation** : question, conversation de session, question de suivi, passages officiels et exemple Python quand il est utile et étayé.
- **API Search** : recherche exacte de l'API présente dans l'index (`json.loads`, `asyncio.gather`, etc.). Les API absentes de la sélection ne sont pas inventées.
- **My Documents** : mode secondaire reprenant l'import PDF, les chunks, embeddings FAISS et réponse Groq ; PDF limité à 10 Mo, 100 pages et 250 000 caractères. Les scans nécessitent un OCR.
- Les embeddings choisis sont optimisés pour l'anglais. Une question française contenant un nom d'API précis bénéficie d'une recherche directe de cette API ; les requêtes françaises purement conceptuelles peuvent être moins fiables.
- Le seuil de similarité `0.35` est heuristique ; une réponse sans passage pertinent est refusée. Le prompt réduit les hallucinations sans les éliminer.
- **Reporté** : Explain Code, Explain Error et autres langages/versions. L'interface ne les affiche pas comme fonctionnalités actives.

# DocQuery

**Developer documentation, explained.** Une application RAG pour explorer une **sélection** de 27 pages de la documentation officielle Python 3.13. Posez une question, consultez les extraits utilisés, recherchez une API précise, expliquez du code ou une erreur, ou interrogez votre propre PDF.

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

Les questions de suivi utilisent la dernière question pour lever une ambiguïté, puis lancent **une nouvelle recherche** dans FAISS. Chaque conversation est conservée dans `st.session_state` pour la durée de la session ; elle disparaît à la fermeture de celle-ci. La recherche d'API est déterministe et utilise les noms/URLs des métadonnées, sans appel Groq.

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

- **Ask Documentation** : chat, nouvelles conversations, questions de suivi, actions « Simplify », « Give example », « Explain deeper ». Chacune relance la recherche FAISS avant Groq. Les conversations restent uniquement en mémoire de session.
- **Langues** : interface en anglais, français ou Darija en alphabet latin (`translations.py`). La langue de la réponse se choisit séparément ; `Auto` demande au modèle de suivre la langue de la dernière question. Le résultat dépend du modèle.
- **API Search** : recherche exacte dans les API indexées, sans appel Groq.
- **Explain Code / Explain Error** : recherche documentaire sur le code ou le traceback, puis explication avec passages officiels. Pour un traceback propre à l'application de l'utilisateur, la documentation peut être insuffisante.
- **Search documentation** : affiche directement les passages FAISS sans appel Groq.
- **My Documents** : import PDF et index FAISS construit seulement quand le fichier change ; 10 Mo, 100 pages et 250 000 caractères maximum. Les scans nécessitent un OCR.
- **Sources** : titre, module, version, extrait exact et URL issue des métadonnées officielles ; le lien ouvre la documentation Python.

Le modèle d'embeddings est optimisé pour l'anglais ; les questions en français et Darija sans nom d'API peuvent retrouver des passages moins fiables. L'index couvre une sélection de pages Python 3.13 et non toute la documentation. La similarité minimale est heuristique. Sans clé Groq, la recherche d'API et la recherche documentaire directe fonctionnent, mais les réponses générées sont indisponibles.

Les options **favoris**, **Darija en alphabet arabe** et l'export des conversations restent à faire. Aucun appel Groq n'est consacré aux traductions de l'interface.

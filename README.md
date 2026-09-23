# DocQuery

**Developer documentation, explained.** Une application RAG pour explorer une **sélection** de 27 pages de la documentation officielle Python 3.13. Posez une question, consultez les extraits utilisés, recherchez une API précise, expliquez du code ou une erreur, ou interrogez votre propre PDF.

L'interface comprend un chat avec saisie fixée en bas de page, une navigation latérale par mode, une recherche directe de documentation sans appel au LLM et un panneau Settings. Le bouton `+` près de la saisie ouvre les raccourcis PDF, code et erreur. Un clic sur une suggestion remplit seulement le champ correspondant : l'utilisateur peut la modifier avant de lancer explicitement la recherche. Les préférences de thème, langue et niveau d'explication sont conservées pendant la session.

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

Les questions de suivi utilisent la dernière question pour lever une ambiguïté, puis lancent **une nouvelle recherche** dans FAISS. Les questions qui citent deux API présentes dans l’index réservent une source pour chacune ; deux comparaisons (`json.load`/`json.loads`, `list.sort`/`sorted`) affichent un tableau uniquement quand les passages étayent les lignes. Chaque conversation est conservée dans `st.session_state` pour la durée de la session ; elle disparaît à la fermeture de celle-ci. La recherche d'API est déterministe et utilise les noms/URLs des métadonnées, sans appel Groq.

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

## Configuration des secrets

Créez une clé sur [GroqCloud](https://console.groq.com/keys). L'application lit `st.secrets["GROQ_API_KEY"]`, puis la variable d'environnement locale :

```bash
export GROQ_API_KEY="votre-cle"           # Linux/macOS
export LOGIN_USERNAME="votre-identifiant"
export LOGIN_PASSWORD="votre-mot-de-passe"
```

```powershell
$env:GROQ_API_KEY = "votre-cle"           # Windows PowerShell
$env:LOGIN_USERNAME = "votre-identifiant"
$env:LOGIN_PASSWORD = "votre-mot-de-passe"
```

Vous pouvez aussi utiliser `.streamlit/secrets.toml`, exclu de Git :

```toml
GROQ_API_KEY = "votre-cle"
LOGIN_USERNAME = "votre-identifiant"
LOGIN_PASSWORD = "votre-mot-de-passe"
```

Le compte unique protège toute l'application. L'identifiant et le mot de passe ne sont jamais écrits dans le code ni publiés sur GitHub. **Ne publiez jamais ces secrets.** Aucune clé OpenAI n'est nécessaire.

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
   LOGIN_USERNAME = "votre-identifiant"
   LOGIN_PASSWORD = "votre-mot-de-passe"
   ```

4. Déployez. `requirements.txt` installe les dépendances et l'application charge l'index versionné dans le dépôt.

## Fonctionnalités et limites

- **Connexion** : un compte unique protège toute l’application. Les identifiants viennent uniquement des Secrets Streamlit ou des variables d’environnement ; le bouton de déconnexion ferme la session sans effacer les préférences visuelles.
- **Ask Documentation** : chat, nouvelles conversations, questions de suivi, actions « Simplify », « Give example », « Explain deeper », « Regenerate », sources repliables et retour utile/pas utile. Les conversations peuvent être renommées ou supprimées et restent uniquement en mémoire de session. Les suggestions initiales et liées préremplissent le composer sans appeler FAISS ni Groq.
- **Langues et réglages** : interface en anglais, français ou Darija en alphabet latin (`translations.py`). La langue de la réponse se choisit séparément ; `Auto` suit la langue de la dernière question. Le thème suit le système par défaut et peut être forcé en clair ou sombre. Le niveau d’explication (débutant, standard, avancé) change le style des réponses, pas les sources. Les exemples de code optionnels et l’ouverture automatique des sources se règlent séparément. Les choix restent disponibles pendant la session.
- **API Search** : recherche exacte dans les API indexées, sans appel Groq. La fiche affiche la signature et les détails effectivement présents dans les métadonnées ; les champs absents ne sont pas complétés artificiellement. La saisie propose des API indexées après quelques caractères.
- **Explain Code / Explain Error** : prompts séparés et réponses concises. Le code est vérifié pour les erreurs de syntaxe sans exécution. « Fix code » demande une correction distincte de l’original lorsqu’une erreur de syntaxe est détectée. Les messages d’erreur et le dernier cadre d’un traceback sont affichés séparément lorsqu’ils sont présents. Les deux modes recherchent leurs passages officiels avant génération ; la documentation peut être insuffisante pour un problème propre à l’application de l’utilisateur.
- **Docs Search** : moteur de recherche qui affiche directement les passages FAISS et leurs liens officiels, sans appel Groq.
- **My Documents** : import PDF, nombre de pages et passages ; index FAISS construit seulement quand le fichier change ; 10 Mo, 100 pages et 250 000 caractères maximum. Les scans nécessitent un OCR.
- **Sources** : titre, module, version, extrait exact et URL issue des métadonnées officielles ; le lien ouvre la documentation Python.

Le modèle d'embeddings est optimisé pour l'anglais ; les questions en français et Darija sans nom d'API peuvent retrouver des passages moins fiables. L'index couvre une sélection de pages Python 3.13 et non toute la documentation. La similarité minimale est heuristique. Sans clé Groq, la recherche d'API et la recherche documentaire directe fonctionnent, mais les réponses générées sont indisponibles.

Les options **réponses enregistrées**, **Darija en alphabet arabe** et l'export des conversations restent à faire. Aucun appel Groq n'est consacré aux traductions de l'interface.

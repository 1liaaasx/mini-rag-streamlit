# Mini RAG PDF avec Streamlit et Groq

Une petite application pédagogique qui répond aux questions sur **un PDF à la fois**. Elle extrait le texte du PDF, recherche les passages proches de votre question et fournit ces passages au modèle Groq `openai/gpt-oss-20b`. Les PDF et les index restent dans la session Streamlit, en mémoire ; ils ne sont pas enregistrés dans le dépôt.

## Architecture RAG

`PDF → extraction PyPDF → nettoyage → chunks avec chevauchement → embeddings locaux → index FAISS → question → recherche des 4 meilleurs passages → contexte → Groq → réponse`

Le modèle `sentence-transformers/all-MiniLM-L6-v2` calcule des embeddings localement, sans clé OpenAI. Les vecteurs sont normalisés ; FAISS utilise leur produit scalaire comme similarité cosinus. Un seuil empirique de `0.20` évite d'envoyer au LLM des passages trop éloignés. Vous pouvez inspecter les passages transmis dans **Voir les sources / passages utilisés**. La réponse reste à vérifier dans le document : le prompt limite les inventions sans garantir leur absence.

## Technologies

| Outil | Rôle |
| --- | --- |
| Streamlit | Interface Web et session utilisateur |
| PyPDF | Extraction du texte des pages PDF |
| Sentence Transformers | Embeddings du document et de la question, calculés localement |
| FAISS (`faiss-cpu`) | Index et recherche de similarité en mémoire |
| Groq (`groq`) | Fournisseur de l'API Chat Completions |
| `openai/gpt-oss-20b` | Identifiant du modèle de génération servi par Groq, **pas** un fournisseur OpenAI ni un modèle d'embeddings |

Le premier chargement des embeddings télécharge le modèle depuis Hugging Face : prévoyez une connexion Internet et un démarrage plus lent. Les téléchargements et les dépendances PyTorch peuvent aussi consommer de la mémoire sur une petite instance Streamlit.

## Installation locale

Python **3.12** est conseillé, également pour le déploiement. Après avoir créé le dépôt GitHub (ou avec son URL réelle) :

```bash
git clone https://github.com/1liaaasx/mini-rag-streamlit.git
cd mini-rag-streamlit
python -m venv .venv
# Linux/macOS : source .venv/bin/activate
# Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

## Configurer Groq

Créez une clé dans [GroqCloud API Keys](https://console.groq.com/keys). Définissez `GROQ_API_KEY` dans votre environnement local :

```bash
# Linux/macOS
export GROQ_API_KEY="votre-cle"
```

```powershell
# Windows PowerShell
$env:GROQ_API_KEY = "votre-cle"
```

Vous pouvez aussi créer localement `.streamlit/secrets.toml` contenant `GROQ_API_KEY = "votre-cle"`. L'application lit d'abord `st.secrets["GROQ_API_KEY"]`, puis la variable d'environnement. `.gitignore` exclut ce fichier de Git ; ne publiez jamais la clé.

## Déployer sur Streamlit Community Cloud

1. Poussez ces fichiers dans un dépôt GitHub.
2. Ouvrez [Streamlit Community Cloud](https://share.streamlit.io/) et créez une application depuis ce dépôt.
3. Choisissez `app.py` comme fichier principal et Python 3.12 dans les paramètres avancés.
4. Dans **Secrets**, ajoutez :

   ```toml
   GROQ_API_KEY = "votre-cle"
   ```

5. Lancez le déploiement. `requirements.txt` installe les dépendances. Le premier démarrage peut prendre plus de temps à cause du modèle d'embeddings.

## Publier le dépôt avec Git

Depuis le dossier `mini-rag-streamlit`, remplacez l'URL ci-dessous par celle de votre dépôt GitHub **déjà créé** :

```bash
git init
git add .
git commit -m "Initial RAG Streamlit app"
git branch -M main
git remote add origin https://github.com/1liaaasx/mini-rag-streamlit.git
git push -u origin main
```

Avant de pousser, vérifiez avec `git status` que `.streamlit/secrets.toml` ou `.env` ne figurent pas dans les fichiers suivis.

## Limites

- Un seul PDF, jusqu'à **10 Mo**, **100 pages**, **250 000 caractères extraits** et **400 passages**. Un nouveau PDF remplace l'index de la session ; les nouvelles questions réutilisent l'index courant.
- Les PDF image ou scannés nécessitent un OCR préalable ; PyPDF n'en fait pas.
- Le modèle d'embeddings proposé est surtout adapté à l'anglais. Pour des documents français, un modèle multilingue améliore souvent la recherche, au prix d'un téléchargement et d'une mémoire plus élevés. Modifier `MODEL_NAME` dans `app.py` permet de l'essayer.
- Le seuil de similarité est heuristique ; une réponse peut être rejetée si les formulations sont très différentes, ou inclure des passages peu utiles.

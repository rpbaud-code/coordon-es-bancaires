# Coordonnées bancaires

Petit formulaire web pour collecter : nom du groupe, IBAN, SWIFT/BIC, nom et lieu de la banque, nom et lieu du titulaire du compte. Les réponses valides s'ajoutent dans `data/reponses.csv`.

## Lancer en local

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
python app.py
```

Ouvrir http://127.0.0.1:5000

## Récupérer les réponses

- En local : ouvrir directement `data/reponses.csv`.
- En ligne (voir ci-dessous) : aller sur `https://<ton-app>.onrender.com/export?token=<ADMIN_TOKEN>` pour télécharger le CSV.

## Héberger gratuitement sur Render

1. Créer un dépôt Git et le pousser sur GitHub :
   ```bash
   git init
   git add .
   git commit -m "Formulaire coordonnées bancaires"
   git remote add origin <url-de-ton-repo-github>
   git push -u origin main
   ```
2. Sur [render.com](https://render.com), créer un compte puis **New > Web Service**, connecter le dépôt GitHub.
3. Configurer :
   - **Build command** : `pip install -r requirements.txt`
   - **Start command** : `gunicorn app:app`
4. Dans **Environment**, ajouter une variable `ADMIN_TOKEN` avec un mot de passe secret de ton choix (sert à protéger `/export`).
5. Déployer. Le lien fourni par Render (`https://xxx.onrender.com`) est celui à envoyer aux gens.

### ⚠️ Important : persistance des données

Sur le plan gratuit de Render, le disque n'est **pas garanti persistant** entre les redéploiements (un `git push` ou un redémarrage du service peut effacer `data/reponses.csv`). Donc :

- Télécharge régulièrement le CSV via `/export?token=...` pendant la période de collecte.
- Évite de redéployer le service tant que tu n'as pas récupéré les réponses.
- Pour une collecte plus longue ou plus critique, envisager un plan payant Render avec disque persistant, ou brancher l'enregistrement sur une base de données externe.

## Sécurité

- `data/reponses.csv` n'est jamais commité dans git (voir `.gitignore`).
- L'export est protégé par un token secret (`ADMIN_TOKEN`), à ne partager avec personne.
- Le site utilise HTTPS automatiquement sur Render.

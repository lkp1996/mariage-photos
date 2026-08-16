# Mariage Luke & Mélissa - Partage de photos

## Installation locale (pour tester avant de déployer)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 app.py
```
Puis ouvre http://localhost:5000

## Déploiement sur Render

1. Crée un dépôt GitHub et pousse ce dossier dedans :
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/TON-USERNAME/mariage-photos.git
   git push -u origin main
   ```

2. Sur [render.com](https://render.com) :
   - "New +" → "Web Service"
   - Connecte le dépôt GitHub `mariage-photos`
   - Build command : `pip install -r requirements.txt`
   - Start command : `gunicorn app:app`
   - Plan : **Starter** (7$/mois)

3. Ajoute un disque persistant (important, sinon les photos disparaissent au redémarrage) :
   - Section "Disks" → Add Disk
   - Mount path : `/opt/render/project/src/uploads`
   - Size : 5 Go

4. Déploie. Tu obtiens une URL du type `https://mariage-photos.onrender.com`

## Après le mariage

Télécharge toutes les photos/vidéos en un ZIP :
```
https://ton-url.onrender.com/download-all/TON-MOT-DE-PASSE-SECRET
```

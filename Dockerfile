# Image de base légère avec Python
FROM python:3.11-slim

# Créer le dossier de travail
WORKDIR /app

# Copier tout le contenu du projet
COPY . .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Lancer le script principal
CMD ["python", "main.py"]

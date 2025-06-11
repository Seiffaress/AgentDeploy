# Image de base légère avec Python
FROM python:3.11-slim

# Créer le dossier de travail
WORKDIR /app

# Copier tout le contenu du projet
COPY . .

# Installer git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Installer les dépendances
RUN pip install --no-cache-dir -r requirement.txt

# Lancer le script principal
CMD ["python", "main.py"]

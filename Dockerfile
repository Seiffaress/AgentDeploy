# Image de base légère avec Python
FROM python:3.11-slim

# Créer le dossier de travail
WORKDIR /app

# Copier tout le contenu du projet
COPY . .

# Installer git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirement.txt

# Lancer l'application FastAPI avec uvicorn (port exposé automatiquement par Render)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

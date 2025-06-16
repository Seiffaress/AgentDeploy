FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirement.txt

CMD ["python", "main.py"]

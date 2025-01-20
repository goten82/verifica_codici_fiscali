# Usa un'immagine di base di Python
FROM python:3.10-slim

# Imposta una directory di lavoro all'interno del container
WORKDIR /app

# Copia i file del progetto nel container
COPY . /app

# Installa le dipendenze del progetto
RUN pip install --no-cache-dir -r requirements.txt

# Specifica il comando di avvio del container
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]


FROM python:3.11-slim

# Instalar dependencias de sistema y pandoc
RUN apt-get update && apt-get install -y curl && \
    curl -L https://github.com/jgm/pandoc/releases/download/3.5/pandoc-3.5-1-amd64.deb -o pandoc.deb && \
    apt-get install -y ./pandoc.deb && \
    rm pandoc.deb && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear directorio app
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

EXPOSE 5000
CMD ["python", "app.py"]

FROM python:3.11-slim

# Instala dependências iniciais
RUN apt-get update && apt-get install -y wget gnupg curl unzip ca-certificates \
    && install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /etc/apt/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Instala as bibliotecas do Python
RUN pip install --no-cache-dir drission-page fastapi uvicorn requests

EXPOSE 10000

# Comando para iniciar a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]

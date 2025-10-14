# Use uma imagem base oficial do Python
FROM python:3.11-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de dependências primeiro (para cache de camadas)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta que a aplicação usa
EXPOSE 8000

# Define o comando para executar a aplicação
CMD ["python", "main.py"]
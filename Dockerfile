# Usar uma imagem base leve do Python
FROM python:3.11-slim

# Definir variáveis de ambiente para otimizar o Python no Docker
# PYTHONDONTWRITEBYTECODE: Previne que o Python escreva arquivos .pyc
# PYTHONUNBUFFERED: Garante que os logs sejam enviados direto para o terminal (importante para observabilidade)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Instalar dependências do sistema operacional (necessário para algumas libs de ML e curl para healthcheck)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código do projeto para dentro do container
COPY ./app/. .   

# Expor as portas usadas pela aplicação
# 8000 = FastAPI (Padrão do Uvicorn)
# 8501 = Streamlit (Interface Visual)
EXPOSE 8000
EXPOSE 8501

# Dar permissão de execução para o script de inicialização
RUN chmod +x start.sh

# Comando padrão para iniciar a aplicação
CMD ["./start.sh"]
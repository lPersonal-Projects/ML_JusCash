#!/bin/bash
set -e # Se der erro em qualquer comando, para o script

# Entra na pasta onde o CodeDeploy jogou os arquivos
cd /home/ubuntu/ML_JusCash

echo "Iniciando containers com Docker Compose..."

# Tenta usar o comando novo (v2) ou o antigo (v1)
if command -v docker-compose &> /dev/null; then
    # Versão antiga (standalone)
    docker-compose up -d --build
else
    # Versão nova (plugin do docker)
    docker compose up -d --build
fi

echo "Deploy finalizado com sucesso!"
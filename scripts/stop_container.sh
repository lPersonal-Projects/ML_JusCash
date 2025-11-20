#!/bin/bash
set -e # Se der erro em qualquer comando, para o script

# Entra na pasta onde o CodeDeploy jogou os arquivos
cd /home/ubuntu/ML_JusCash || exit 0

echo "Parando containers antigos..."

# Tenta derrubar o compose anterior
if command -v docker-compose &> /dev/null; then
    docker-compose down || true
else
    docker compose down || true
fi
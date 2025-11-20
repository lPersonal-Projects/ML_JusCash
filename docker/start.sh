#!/bin/bash

# Iniciar o Backend (API FastAPI) em segundo plano
# O host 0.0.0.0 é necessário para ser acessível fora do container
echo "Iniciando API..."
uvicorn main:app --host 0.0.0.0 --port 8000 &

# Iniciar o Frontend (Streamlit) em primeiro plano
echo "Iniciando Interface Visual..."
streamlit run ui.py --server.port 8501 --server.address 0.0.0.0
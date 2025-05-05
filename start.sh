#!/usr/bin/env bash
set -e

# 1) Démarrage de l'API FastAPI
uvicorn main:app --host 0.0.0.0 --port 8001 &
sleep 3
# 2) Démarrage de Streamlit
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port ${PORT:-8000}
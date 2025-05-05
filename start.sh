#!/usr/bin/env bash
set -e

# 1) Démarrage de l'API FastAPI
uvicorn main:app --host 0.0.0.0 --port 8000 &

# 2) Démarrage de Streamlit
streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port ${PORT:-8501}
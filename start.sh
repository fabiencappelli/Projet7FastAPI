#!/usr/bin/env bash
set -e
# 1) Démarrage de l'API FastAPI
uvicorn main:app --host 0.0.0.0 --port 8001 &
# 2) Attends que le backend soit up
while ! nc -z localhost 8001; do sleep 1; done
# 23) Démarrage de Streamlit
streamlit run streamlit_app.py --server.port ${PORT:-8000} --server.enableCORS false
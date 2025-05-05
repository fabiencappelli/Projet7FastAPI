"""
streamlit run streamlit_app.py
"""
import streamlit as st
import requests
import json

#API_URL = "http://127.0.0.1:8000"
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Text Classification Tester", layout="wide")

st.title("Interface de test pour l'API de classification de texte")
st.write("Utilisez cette interface pour envoyer des requêtes à votre API FastAPI en local.")

endpoint = st.selectbox(
    "Sélectionnez l'endpoint à appeler", 
    ("/predict", "/predict/format")
)

st.markdown("---")
st.write("Entrez vos textes ci-dessous, un par ligne (en anglais !)")

input_text = st.text_area(
    label="Vos textes :", 
    value="This trip was terrible, I thought the plane would crash before even taking off", 
    height=200
)

if st.button("Envoyer la requête"):
    st.markdown("---")
    # Préparation du payload JSON
    texts = [line.strip() for line in input_text.splitlines() if line.strip()]
    payload = {"texts": texts}

    # Appel de l'API
    try:
        response = requests.post(f"{API_URL}{endpoint}", json=payload)
        response.raise_for_status()
        results = response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")
    else:
        # Affichage brut
        st.subheader("Réponse brute JSON")
        st.json(results)

        # Présentation sous forme de tableau
        st.subheader("Résultats formatés")
        # Conversion en DataFrame pour affichage
        try:
            import pandas as pd
            df = pd.DataFrame(results)
            st.table(df)
        except Exception:
            st.warning("Impossible d'afficher le tableau. Affichage JSON uniquement.")
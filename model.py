from pathlib import Path
import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Répertoire de base et nom du fichier modèle
BASE_DIR = Path(__file__).resolve().parent
MODEL_FILE = BASE_DIR / "text_clf_pipeline.joblib"


def train(
    file_path: str = BASE_DIR / "df_cleaned.csv",
    text_col: str = "text",
    label_col: str = "target"
) -> bool:
    """
    Entraîne un pipeline TF-IDF + régression logistique à partir d'un fichier CSV.

    Arguments:
    - file_path : chemin vers le fichier CSV contenant df_cleaned
    - text_col  : nom de la colonne de texte
    - label_col : nom de la colonne de labels (0/1)

    Retourne True si l'entraînement et la sauvegarde réussissent.
    """
    # Chargement du DataFrame
    csv_path = Path(file_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier non trouvé : {file_path}")

    df = pd.read_csv(csv_path, encoding='latin-1')
    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Colonnes attendues '{text_col}' et '{label_col}' manquantes dans le fichier CSV")

    # Construction du pipeline
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_df= 0.8, min_df=0.02, ngram_range=(1, 1))),
        ("clf", LogisticRegression(solver="liblinear", C=10))
    ])

    # Entraînement
    pipeline.fit(df[text_col], df[label_col])

    # Sauvegarde
    joblib.dump(pipeline, MODEL_FILE)
    return True


def predict(texts: list[str]) -> list[dict]:
    """
    Prédit labels et probabilités sur une liste de textes.
    """
    if not MODEL_FILE.exists():
        raise FileNotFoundError("Modèle non trouvé : appelez d'abord train_from_file()")

    pipeline = joblib.load(MODEL_FILE)
    probs = pipeline.predict_proba(texts)[:, 1]
    labels = pipeline.predict(texts)

    results = []
    for txt, lab, p in zip(texts, labels, probs):
        results.append({"text": txt, "label": int(lab), "prob": float(p)})
    return results


def convert(
    results: list[dict],
    mapping: dict = {0: "negatif", 1: "positif"}
) -> list[dict]:
    """
    Convertit la sortie brute en labels textuels.
    """
    out = []
    for r in results:
        out.append({
            "text": r["text"],
            "label": mapping.get(r["label"], str(r["label"])),
            "probabilite": r["prob"]
        })
    return out

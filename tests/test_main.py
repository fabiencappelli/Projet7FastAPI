import pytest
from fastapi import HTTPException
import main
from main import predict_api, TextsIn

def test_predict_api_success(monkeypatch):

    dummy = [
        {"text": "oui", "label": 1, "prob": 0.42},
        {"text": "non", "label": 0, "prob": 0.17},
    ]

    monkeypatch.setattr(main, "predict", lambda texts: dummy)
    # écrire un lambda texts: dummy est plus rapide qu’une fonction complète def fake_predict(texts): return dummy
    # la signature originale de predict est def predict(texts: list[str]). 
	# Pour que notre fake ait la même signature minimale (même si on n’utilise pas texts), on écrit lambda texts: …
    
    payload = TextsIn(texts=["oui", "non"])
    
    result = predict_api(payload)
    
    assert result == dummy


def test_predict_api_model_not_found(monkeypatch):

    def fake_predict(texts):
        raise FileNotFoundError("Modèle introuvable")
    
    monkeypatch.setattr(main, "predict", fake_predict)
    
    payload = TextsIn(texts=["x"])
    
    with pytest.raises(HTTPException) as excinfo:
        predict_api(payload)
    
    err = excinfo.value
    assert err.status_code == 404
    assert "modèle introuvable" in err.detail.lower()




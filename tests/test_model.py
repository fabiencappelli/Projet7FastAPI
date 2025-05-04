import model

def test_convert_translates_labels_correctly():
    raw = [
        {"text": "t1", "label": 0, "prob": 0.1},
        {"text": "t2", "label": 1, "prob": 0.9},
    ]
    formatted = model.convert(raw)

    assert formatted[0]["label"] == "negatif"
    assert formatted[1]["label"] == "positif"
    # s’assure que la probabilité reste inchangée
    assert formatted[0]["probabilite"] == 0.1
    assert formatted[1]["probabilite"] == 0.9
    # s’assure que le texte reste inchangé
    assert formatted[0]["text"] == "t1"
    assert formatted[1]["text"] == "t2"

def test_predict_returns_expected_structure():
    texts = ["oui", "non"]
    results = model.predict(texts)

    assert isinstance(results, list)
    assert len(results) == 2
    for item in results:
        assert set(item.keys()) == {"text", "label", "prob"}
        assert isinstance(item["text"], str)
        assert isinstance(item["label"], int)
        assert isinstance(item["prob"], float)
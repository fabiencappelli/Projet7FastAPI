"""
Lancer le serveur uvicorn main:app --reload
"""
from fastapi import FastAPI, HTTPException
from model import convert, predict
from pydantic import BaseModel

app = FastAPI(title="Classification de tweets API")

class TextsIn(BaseModel):
	texts: list[str]

class RawPrediction(BaseModel):
	text: str
	label: int
	prob: float

class FormattedPrediction(BaseModel):
	text: str
	label: str
	probabilite: float


@app.get("/ping")
def pong():
	return {"ping": "pong!"}

@app.post(
    "/predict",
    response_model=list[RawPrediction],
    status_code=200
)
def predict_api(payload: TextsIn):
    try:
        results = predict(payload.texts)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return results

@app.post(
    "/predict/format",
    response_model=list[FormattedPrediction],
    status_code=200
)
def predict_formatted_api(payload: TextsIn):
    try:
        results = predict(payload.texts)
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    formatted = convert(results)
    return formatted
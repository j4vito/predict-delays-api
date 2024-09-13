from fastapi import FastAPI, HTTPException
from challenge.model import DelayModel
import pandas as pd
import json

dm = DelayModel()
data = pd.read_csv("data/data.csv")
features, target = dm.preprocess(data, target_column="delay")
dm.fit(features, target)
app = FastAPI()

@app.get("/", status_code=200)
async def get_root() -> dict:
    return {
        "message": "Welcome to the Delays API"
    }

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(data: dict) -> dict:
    dataframe = pd.DataFrame(data["flights"])
    features = dm.preprocess(dataframe)
    if features is None:
        print("FEATURES IS NONE")
        raise HTTPException(status_code=400, detail="Unknown columns")

    pred = dm.predict(features)
    return {
        "predict": pred
    }

#define initial funtion for training the model

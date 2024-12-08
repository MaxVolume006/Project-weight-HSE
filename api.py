from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from back import predict_weight, linr, coder

class AddRowRequestForm(BaseModel):
    Age: int
    Gender: str
    Current_Weight: float
    BMR: float
    Daily_Consumed: float
    Daily_Change: float
    Weight_Change: float
    Duration: int
    Activity: str
    Sleep: str
    Stress: int
    Final_Weight: int

class WeightRequestForm(BaseModel):
    Age: int
    Gender: str
    Current_Weight_kg: float
    BMR_Calories: float
    Daily_Calories_Consumed: float
    Duration_weeks: int
    Physical_Activity_Level: str


app = FastAPI(docs_url='/')


@app.post('/weight')
async def weight_prediction(data: WeightRequestForm):
    ans: float = predict_weight(data.json(), linr, coder)
    print(ans)
    return {
        "result": ans
    }
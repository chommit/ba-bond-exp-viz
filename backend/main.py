from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend URL, # FIXME Might increment
    allow_credentials=True,
    allow_methods=["*"],  # Allow POST, OPTIONS, GET, etc.
    allow_headers=["*"],
)


class GiftInput(BaseModel):
    gift_id: int
    value: int  # 1=nice, 2=great, 3=amazing

class ComputeRequest(BaseModel):
    gifts: List[GiftInput]

def compute_exp_per_month(gift_vector):
    # Replace with your real function
    components = [random.randint(800, 2200) for _ in range(6)]
    return components

@app.post("/compute")
def compute(req: ComputeRequest):
    gift_vector = [0] * 48
    for g in req.gifts:
        gift_vector[g.gift_id - 1] = g.value

    components = compute_exp_per_month(gift_vector)
    total = sum(components)

    return {
        "total_exp": total,
        "components": components
    }

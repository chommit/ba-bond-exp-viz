from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random
from fastapi.middleware.cors import CORSMiddleware

from compute import compute_bond_exp_per_month_comp

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

@app.post("/compute")
def compute(req: ComputeRequest):
    bond_exp_components = compute_bond_exp_per_month_comp(req)
    total = bond_exp_components["Total EXP"]
    del bond_exp_components["Total EXP"]

    return {
        "total_exp": total,
        "components": bond_exp_components
    }


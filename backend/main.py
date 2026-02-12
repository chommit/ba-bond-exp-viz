from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random
from fastapi.middleware.cors import CORSMiddleware

from compute import compute_bond_exp_per_month

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
    bond_exp_comp_arr = compute_bond_exp_per_month(req)
    total = bond_exp_comp_arr[-1]
    bond_exp_comp_arr = bond_exp_comp_arr[:-1]

    return {
        "total_exp": total,
        "components": bond_exp_comp_arr
    }


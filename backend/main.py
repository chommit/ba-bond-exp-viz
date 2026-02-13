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


class Params(BaseModel):
    dailyHeadpats: float
    craftingMonthlies: bool
    giftMonthlies: bool
    eligmaMiniKeystones: bool
    redBouquetPacks: int
    frrTryhard: bool


class ComputeRequest(BaseModel):
    gifts: List[GiftInput]
    params: Params


@app.post("/compute")
def compute(req: ComputeRequest):
    params = req.params
    student_gift_prefs = req.gifts
    bond_exp_comp_arr = compute_bond_exp_per_month(student_gift_prefs, 
                                                   num_daily_headpats=params.dailyHeadpats,
                                                   crafting_monthlies=params.craftingMonthlies,
                                                   gift_monthlies=params.giftMonthlies,
                                                   eligma_mini_keystones=params.eligmaMiniKeystones,
                                                   frr_tryhard=params.frrTryhard,
                                                   num_red_bouquet_packs_per_year=params.redBouquetPacks)
    total = bond_exp_comp_arr[-1]
    exp_per_craft = bond_exp_comp_arr[-2]
    bond_exp_comp_arr = bond_exp_comp_arr[:-2]

    return {
        "total_exp": total,
        "components": bond_exp_comp_arr,
        "exp_per_craft": exp_per_craft
    }


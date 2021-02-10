from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


class FaucetRequest(BaseModel):
    targetAddress: str
    amt: float


app = FastAPI()


@app.get("/")
def root():
    return {"message": "You have reached... duhh.. cheapeth faucet api"}


@app.post("/request")
def read_user(request: FaucetRequest):
    return {"message": "You fuckin got it chief"}

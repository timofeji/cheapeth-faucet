from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from web3 import Web3, HTTPProvider
from solcx import compile_files

#ganache boy
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

compiled_sol = compile_files(['../contracts/faucet.sol'])
deployment_compiled = compiled_sol['../contracts/faucet.sol:faucet']
deployment = w3.eth.contract(abi=deployment_compiled['abi'], bytecode=deployment_compiled['bin'])

tx_hash = deployment.constructor().transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

faucet = w3.eth.contract(address=tx_receipt.contractAddress, abi=deployment_compiled['abi'])

tx_hash = faucet.functions.fundFaucet().transact(
    {'from': w3.eth.accounts[0], 'value': 10000000000000000000})
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

rich_logs = faucet.events.received().processReceipt(tx_receipt)
rich_logs[0]['args']
print(rich_logs)

class FaucetRequest(BaseModel):
    address: str
    amt: float


app = FastAPI()


@app.get("/")
def root():
    return {"message": "You have reached... uhh.. the cheapeth faucet api"}


@app.post("/request")
def read_user(request: FaucetRequest):
    address = Web3.toChecksumAddress(request.address)
    tx_hash = faucet.functions.sendFunds(address, 1000).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    rich_logs = faucet.events.sent().processReceipt(tx_receipt)
    rich_logs[0]['args']
    print(rich_logs)
    return {"message": "YOU GOT IT CHIEF"}

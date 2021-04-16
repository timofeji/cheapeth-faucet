from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from web3 import Web3, HTTPProvider
from solcx import compile_files

import time
import os
import atexit
import json
from json.decoder import JSONDecodeError


#I can do this cuz cheapeth cheap jk lol
DEPLOYER_PRIVATE_KEY = os.environ.get('DEPLOYER_PRIVATE_KEY')

DEPLOYER_ADDRESS = os.environ.get('DEPLOYER_ADDRESS')

print(DEPLOYER_PRIVATE_KEY)
print(DEPLOYER_ADDRESS)

FAUCET_CONTRACT_ADDRESS = '0xc2d39907accfc3951e915b30a8f5d03a35b29071'
COOLDOWN_PERIOD = 864000  # 10 days
COOLDOWN_FILENAME = 'cooldowns.json'

cooldowns = {}
cooldowns_ip = {}
if(os.path.exists(COOLDOWN_FILENAME)):
    with open(COOLDOWN_FILENAME) as f:
        try:
            cooldowns = json.load(f)
        except JSONDecodeError:
            pass


def exit_handler():
    js = json.dumps(cooldowns)
    f = open(COOLDOWN_FILENAME, "w")
    f.write(js)
    f.close()


atexit.register(exit_handler)

test_acc = Web3.toChecksumAddress(DEPLOYER_ADDRESS)
#connect to cheap node
w3 = Web3(Web3.HTTPProvider('https://node.cheapeth.org/rpc'))
w3.eth.default_account = test_acc

compiled_sol = compile_files(['../contracts/faucet.sol'])
faucet_compiled = compiled_sol['../contracts/faucet.sol:faucet']

faucet_address = Web3.toChecksumAddress(FAUCET_CONTRACT_ADDRESS)
faucet = w3.eth.contract(faucet_address, abi=faucet_compiled['abi'])

class FaucetRequest(BaseModel):
    address: str
    amt: float

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://www.faucet.cheap",
    "http://faucet.cheap"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/test")
def root():
    return {"message": "You have reached... uhh.. the cheapeth faucet api"}


@app.post("/api/request")
def read_user(request: FaucetRequest, req: Request):
    client_host = req.client.host
    
    if(client_host in cooldowns_ip and (cooldowns_ip[client_host] + COOLDOWN_PERIOD) > time.time()):
        raise HTTPException(status_code=425, detail='OY OY slow down boYE')

    amt = Web3.toWei(request.amt, 'ether')
    if(amt > Web3.toWei(1, 'ether')):
        raise HTTPException(status_code=425, detail='Faucet broke pls only requests under 1cth')


    address = Web3.toChecksumAddress(request.address)
    if(address in cooldowns and (cooldowns[address] + COOLDOWN_PERIOD) > time.time()):
        raise HTTPException(status_code=425, detail='OY OY slow down boYE')

    nonce = w3.eth.getTransactionCount(test_acc)  
    tx_hash = faucet.functions.sendFunds(address, amt).buildTransaction({'chainId': 777,'gas': 300000,'gasPrice': w3.toWei('1', 'gwei'),'nonce': nonce,})
    print(tx_hash)
    signed_txn = w3.eth.account.sign_transaction(tx_hash, private_key=DEPLOYER_PRIVATE_KEY)


    w3.eth.sendRawTransaction(signed_txn.rawTransaction)

    cooldowns[address] = time.time()
    cooldowns_ip[client_host] = time.time()
    return {"message": "YOU GOT IT CHIEF 🍆"}


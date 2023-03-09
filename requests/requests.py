import uvicorn
from fastapi import FastAPI
from enum import Enum

HOST = '127.0.0.1'
PORT = 8000

app = FastAPI()

# Path Parameters
#  * Default
@app.get("/path_items/name/{item_name}")
async def read_item(item_name):
    return {"item_name": item_name}

#  * With Type
@app.get("/path_items/id/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

#  * Enum
class CryptoSymbol(str, Enum):
    BTC = "btc"
    ETH = "eth"


@app.get("/crypto/{crypto_symbol}")
async def get_crypto(crypto_symbol : CryptoSymbol):
    if crypto_symbol is CryptoSymbol.BTC:
        return {"crypto_symbol" : CryptoSymbol.BTC.value, "message" : "Bitcoin"}
    
    if crypto_symbol.value == "eth":
        return {"crypto_symbol" : CryptoSymbol.ETH.value, "message" : "Etherum"}

    return {"crypto_symbol" : "Unknown", "message" : "Unknown symbol!"}


# ***********************************************************************************

# Query Parameters

@app.get("/items/query/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# ***********************************************************************************

# Request Body

from fastapi import status
from pydantic import BaseModel

class Item(BaseModel):
    name: str                       # Required
    description: str | None = None  # Not Required
    price: float                    # Required
    tax: float | None = None        # Not Required


@app.post("/items/body/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item



# ***********************************************************************************

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)
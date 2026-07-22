import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

items: dict[str, "Item"] = {}


class ItemCreate(BaseModel):
    name: str
    price: float


class Item(ItemCreate):
    id: str


@app.post("/items", status_code=201)
def create_item(item: ItemCreate) -> Item:
    new_item = Item(id=str(uuid.uuid4()), **item.model_dump())
    items[new_item.id] = new_item
    return new_item


@app.get("/items/{item_id}")
def get_item(item_id: str) -> Item:
    item = items.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

from fastapi.applications import FastAPI
from pydantic import BaseModel
from typing import Union

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    price_with_tax: Union[float, None] = None


fake_data = {
    "name": "Foo",
    "description": "An optional description",
    "price": 45.2,
    "tax": 3.5,
}


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/items", response_model=Item)
async def get_items():
    return Item(
        name=fake_data["name"],
        description=fake_data["description"],
        price=fake_data["price"],
        tax=fake_data["tax"],
    )


@app.post("/items", response_model=Item)
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

from typing import List

from fastapi import APIRouter
from schema.item_schema import Item

routes: APIRouter = APIRouter()

@routes.post('/', response_model= Item)
async def create_item(item: Item) -> Item:
    """ Create new item"""
    result = await item.create()
    return result

@routes.get('/', response_model=List[Item])
async def get_all_item() -> List[Item]:
    """ Get all exisiting item """
    items = await Item.find_all().to_list()
    return items
from typing import List
from fastapi import FastAPI
from schema.item_schema import Item
from config import initDB
from routes import items_routes, users_routes


app = FastAPI()

@app.on_event("startup")
async def app_init():
    """ initialize Mongodb and add routes """
    await initDB()
    app.include_router(items_routes.routes, prefix="/v1", tags=["items"])
    app.include_router(users_routes.routes, prefix="/auth",tags=["users"])



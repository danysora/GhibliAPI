from pymongo import MongoClient
from fastapi import FastAPI
import contextlib

MONGO_URI = "mongodb://localhost/pythonmongodb"

@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.mongo_client = MongoClient(MONGO_URI)
    app.state.database = app.state.mongo_client.get_database()
    yield
    app.state.mongo_client.close()
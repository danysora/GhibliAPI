from fastapi import FastAPI
from .database import lifespan
from .routers import ghibli, usuarios

app = FastAPI(lifespan=lifespan)

app.include_router(usuarios.router)
app.include_router(ghibli.router)
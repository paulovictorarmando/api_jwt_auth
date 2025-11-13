from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.UsuarioController import router as usuario_router
from config.connection import create_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
	create_tables()
	yield

app = FastAPI(lifespan=lifespan)
app.include_router(usuario_router)

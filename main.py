from fastapi import FastAPI
from contextlib import asynccontextmanager
from controller.UsuarioController import router as usuario_router
from config.connection import create_tables

from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
	create_tables()
	yield

app = FastAPI(lifespan=lifespan)
app.include_router(usuario_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ou a origem específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

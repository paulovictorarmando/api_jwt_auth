from sqlmodel import SQLModel, create_engine, Session
from .settings import ENV

engine = create_engine(ENV.DATABASE_URL, echo=True)

def create_tables():
	SQLModel.metadata.create_all(engine)

def get_session():
	with Session(engine) as s:
		yield s
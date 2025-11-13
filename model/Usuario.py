from sqlmodel import SQLModel, Field
from typing import Optional

class Usuario(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	username: str = Field(max_length=50, nullable=False)
	email: str = Field(unique=True, nullable=False)
	senha: str = Field(nullable=False)

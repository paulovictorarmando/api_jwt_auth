from pydantic import BaseModel, EmailStr, Field
from typing import Annotated, Optional

class UsuarioRead(BaseModel):
	id: int
	username: str
	email: Optional[str] = None
	model_config = {"from_attributes": True}

class UsuarioCreate(BaseModel):
	username: Annotated[str, Field(max_length=50)]
	email: EmailStr
	senha: Annotated[ str, Field(min_length=5)] = None

class UsuarioLogin(BaseModel):
	email: EmailStr
	senha: str

class UsuarioUpdate(BaseModel):
	username: Optional[Annotated[str, Field(max_length=50)]] = None
	email: Optional[EmailStr] = None
	senha: Optional[Annotated[str, Field(min_length=5)]] = None
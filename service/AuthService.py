from jose import jwt, JWTError
from sqlmodel import Session
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from model.Usuario import Usuario
from repository.UsuarioRepository import UsuarioRepository
from config.connection import get_session
from config.settings import ENV
from dto.UsuarioDTO import UsuarioLogin

hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

class AuthService:
	@staticmethod
	def create_hash(password: str) -> str:
		return hash_context.hash(password)


	@staticmethod
	def verify_hash(password: str, hashed: str) -> bool:
		return hash_context.verify(password, hashed)

	@staticmethod
	def token_encode(data: dict) -> str:
		encode = data.copy()
		expire = datetime.now(timezone.utc) + timedelta(minutes=ENV.ACCESS_TOKEN_EXPIRE_MINUTES)
		encode.update({"exp": expire})
		return jwt.encode(encode, ENV.SECRET_KEY, algorithm=ENV.ALGORITHM)
	
	@staticmethod
	def token_decode(token: str) -> dict | None:
		try:
			return jwt.decode(token, ENV.SECRET_KEY, algorithms=[ENV.ALGORITHM])
		except JWTError:
			return None
	
	@staticmethod
	def login(session: Session, uLogin: UsuarioLogin) -> dict:
		usuario = UsuarioRepository.getByEmail(session, uLogin.email)
		if not usuario or not AuthService.verify_hash(uLogin.senha, usuario.senha):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Credenciais inválidas"
			)
		token = AuthService.token_encode({"sub": str(usuario.id)})
		return {"access_token": token, "token_type": "bearer"}

	@staticmethod
	def get_user(
		token: str = Depends(oauth2_scheme),
		s: Session = Depends(get_session)
	) -> Usuario | None:
		try:
			payload = AuthService.token_decode(token)
			id: str = payload.get("sub")
		except JWTError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido",
				headers={"WWW-Authenticate": "Bearer"}
			)
		except AttributeError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido",
				headers={"WWW-Authenticate": "Bearer"}
			)
		usuario = UsuarioRepository.getById(s, int(id))
		if not usuario:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token inválido",
				headers={"WWW-Authenticate": "Bearer"}
			)
		return usuario
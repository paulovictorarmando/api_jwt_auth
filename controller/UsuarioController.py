from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from service.UsuarioService import UsuarioService
from service.AuthService import AuthService
from config.connection import get_session
from dto.UsuarioDTO import UsuarioCreate, UsuarioLogin, UsuarioUpdate, UsuarioRead
from model.Usuario import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(usuarioCreate: UsuarioCreate, session: Session = Depends(get_session)) -> Usuario:
	try:
		return UsuarioService.create(session, usuarioCreate)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}", response_model=UsuarioRead, status_code=status.HTTP_200_OK)
def update_usuario(id: int,
	usuarioUpdate: UsuarioUpdate,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_user)) -> UsuarioRead | None:
	try:
		if usuario.id != id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado")
		return UsuarioRead.model_validate(UsuarioService.update(session, id, usuarioUpdate))
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(id: int,
	session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_user)) -> None:
	try:
		if usuario.id != id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado")
		UsuarioService.delete(session, id)
		return
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me/", response_model=UsuarioRead, status_code=status.HTTP_200_OK)
def me(session: Session = Depends(get_session),
	usuario: Usuario = Depends(AuthService.get_user)) -> UsuarioRead:
	return UsuarioRead.model_validate(UsuarioService.me(session, usuario))

@router.post("/login/", status_code=status.HTTP_200_OK)
def login(usuario: UsuarioLogin, session: Session = Depends(get_session)):
	try:
		return AuthService.login(session, usuario)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
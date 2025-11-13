from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session
from service.UsuarioService import UsuarioService
from service.AuthService import AuthService
from config.connection import session
from dto.UsuarioDTO import UsuarioCreate, UsuarioUpdate, UsuarioRead
from model import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(usuarioCreate: UsuarioCreate, session: Session = Depends(session)) -> Usuario:
	try:
		return UsuarioService.create(session, usuarioCreate)
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{id}", response_model=UsuarioRead, status_code=status.HTTP_200_OK)
def update_usuario(id: int,
	usuarioUpdate: UsuarioUpdate,
	session: Session = Depends(session),
	usuario: Usuario = Depends(AuthService.get_user)) -> UsuarioRead | None:
	try:
		if usuario.id != id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado")
		return UsuarioRead.model_validate(UsuarioService.update(session, id, usuarioUpdate))
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{id}", model_return_annotation=UsuarioRead, status_code=status.HTTP_204_NO_CONTENT)
def delete_usuario(id: int,
	session: Session = Depends(session),
	usuario: Usuario = Depends(AuthService.get_user)) -> UsuarioRead | None:
	try:
		if usuario.id != id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuário não autorizado")
		return UsuarioRead.model_validate(UsuarioService.delete(session, id))
	except ValueError as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/me", response_model=UsuarioRead, status_code=status.HTTP_200_OK)
def me(session: Session = Depends(session),
	usuario: Usuario = Depends(AuthService.get_user)) -> UsuarioRead:
	return UsuarioRead.model_validate(UsuarioService.me(session, usuario))	
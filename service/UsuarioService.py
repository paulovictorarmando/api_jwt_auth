from .AuthService import AuthService
from repository.UsuarioRepository import UsuarioRepository

from model import Usuario
from dto.UsuarioDTO import UsuarioCreate, UsuarioUpdate, UsuarioRead
from sqlmodel import Session

class UsuarioService:
	@staticmethod
	def create(session: Session, usuarioCreate: UsuarioCreate) -> Usuario:
		if UsuarioRepository.getByEmail(session, usuarioCreate.email):
			raise ValueError("Email já cadastrado")
		usuarioCreate.senha = AuthService.create_hash(usuarioCreate.senha)
		usuario = UsuarioRepository.crete(session, usuarioCreate)
		return UsuarioRead.model_validate(usuario)
	
	@staticmethod
	def update(session: Session, id: int, usuarioUpdate: UsuarioUpdate) -> Usuario:
		usuario = UsuarioRepository.getById(session, id)
		if not usuario:
			raise ValueError("Usuário não encontrado")
		if usuarioUpdate.senha:
			usuarioUpdate.senha = AuthService.create_hash(usuarioUpdate.senha)
		usuario = UsuarioRepository.update(session, id, usuarioUpdate)
		return UsuarioRead.model_validate(usuario)
	
	@staticmethod
	def delete(session: Session, id: int) -> Usuario:
		usuario = UsuarioRepository.getById(session, id)
		if not usuario:
			raise ValueError("Usuário não encontrado")
		usuario = UsuarioRepository.delete(session, id)
		return UsuarioRead.model_validate(usuario)
	
	@staticmethod
	def me(session: Session, usuario: Usuario) -> Usuario:
		return UsuarioRead.model_validate(usuario)
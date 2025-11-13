from sqlmodel import Session, select
from model.Usuario import Usuario
from dto.UsuarioDTO import UsuarioCreate, UsuarioUpdate

class UsuarioRepository:
	@staticmethod
	def getById(session: Session, id: int) -> Usuario | None:
		return session.get(Usuario, id)

	@staticmethod
	def getByEmail(session: Session, email: str) -> Usuario | None:
		return session.exec(select(Usuario).where(Usuario.email==email)).first()

	@staticmethod
	def crete(session: Session, usuarioCreate: UsuarioCreate) -> Usuario:
		usuario = Usuario(**usuarioCreate.model_dump())
		session.add(usuario)
		session.commit()
		session.refresh(usuario)
		return usuario

	@staticmethod
	def update(session: Session, id:int, usuarioUpdate: UsuarioUpdate) -> Usuario | None:
		usuario = session.get(Usuario, id)
		if not usuario:
			return None
		dados = usuarioUpdate.model_dump(exclude_unset=True)
		for k, v in dados.items():
			setattr(usuario, k, v)
		session.add(usuario)
		session.commit()
		session.refresh(usuario)
		return usuario
	
	@staticmethod
	def delete(session: Session, id: int) -> Usuario | None:
		usuario = session.get(Usuario, id)
		if not usuario:
			return None
		session.delete(usuario)
		session.commit()
		return usuario

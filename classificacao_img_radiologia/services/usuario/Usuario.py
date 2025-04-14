from db import DatabaseSession
from models import Usuario
import traceback

from sqlalchemy import or_, select

class UsuarioService:
    
    @staticmethod
    def register(nome:str, usuario:str, senha:str, email:str, matricula:str=None, curso:str=None, session=None) -> list:
        if not session:
            db = DatabaseSession()
            session = db.get_session()
        
        try:
            # Criptografar senha.
            statement = select(Usuario).where(
                or_(
                    Usuario.email == email,
                    Usuario.matricula == matricula,
                    Usuario.usuario == usuario
                )
            )
            user_exist = session.scalar(statement)
            if user_exist:
                matched = []
                if user_exist.email == email:
                    matched.append("email")
                if user_exist.matricula == str(matricula):
                    matched.append("matricula")
                if user_exist.usuario == usuario:
                    matched.append("usuario")

                return [False, "Já existe um usuário com esse(s) dado(s): " + ", ".join(matched)]
            user = Usuario(nome=nome, usuario=usuario, senha=senha, email=email, matricula=matricula, curso=curso)
            session.add(user)
            session.commit()
            return [True, user]
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return [False, e]
            
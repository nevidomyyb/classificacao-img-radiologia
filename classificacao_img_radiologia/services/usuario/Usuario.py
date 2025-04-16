from db import DatabaseSession
from models import Usuario
from sqlalchemy import or_, select

import hashlib
import traceback

class UsuarioService:
    
    @staticmethod 
    def check_password(plain_password: str, saved_password: str):
        hashed_pass = hashlib.sha256(plain_password.encode()).hexdigest()
        return hashed_pass == saved_password
    
    @staticmethod
    def login(username: str, password: str, session=None):
        if not session:
            db = DatabaseSession()
            session = db.get_session()
        
        try:
            statement = select(Usuario).where(Usuario.usuario == username)
            user = session.scalar(statement)
            if not user:
                return [False, "Usuário ou senha inválidos."]
            if  UsuarioService.check_password(password, user.senha):
                return [True, user]
            else:
                return [False, "Usuário ou senha inválidos."]
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return [False, e]
        
    
    @staticmethod
    def register(nome:str, usuario:str, senha:str, email:str, matricula:str=None, curso:str=None, session=None) -> list:
        if not session:
            db = DatabaseSession()
            session = db.get_session()
        
        try:
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
            senha_hashed = hashlib.sha256(senha.encode()).hexdigest()
            user = Usuario(nome=nome, usuario=usuario, senha=senha_hashed, email=email, matricula=matricula, curso=curso)

            session.add(user)
            session.commit()
            return [True, user]
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            return [False, e]
            
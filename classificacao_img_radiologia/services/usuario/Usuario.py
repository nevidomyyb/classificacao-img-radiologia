from db import DatabaseSession
from models import Usuario
from sqlalchemy import or_, select
from dotenv import load_dotenv
from services.CookieManager import CookieManager

import hashlib
import traceback
import os

class UsuarioService:
    
    @staticmethod 
    def check_password(plain_password: str, saved_password: str):
        hashed_pass = hashlib.sha256(plain_password.encode()).hexdigest()
        return hashed_pass == saved_password
    
    @staticmethod
    def get_user_id_by_cookie():
        CManager = CookieManager()
        USERNAME = CManager.get_cookie_manager().get('AUTH_USERNAME_UNCISAL')
        db = DatabaseSession()
        session = db.get_session()
        try:
            user_id = session.execute(select(Usuario.id).where(Usuario.usuario == USERNAME)).scalar()
            return user_id
        except:
            session.rollback()
            traceback.print_exc()
            return None
    @staticmethod
    def logout():
        CManager = CookieManager()
        CManager.get_cookie_manager().delete('AUTH_COOKIE_UNCISAL', key='delete-0')
        CManager.get_cookie_manager().delete('AUTH_USERNAME_UNCISAL', key='delete-1')
    
    @staticmethod
    def create_login_cookie(username:str):
        load_dotenv()
        SALT = os.getenv('COOKIE_SALT')
        cookie = f'{username}:{SALT}'
        hashed_cookie = hashlib.sha256(cookie.encode()).hexdigest()
        return hashed_cookie
    
    @staticmethod
    def get_name_from_cookie():
        CManager = CookieManager()
        username = CManager.get_cookie_manager().get('AUTH_USERNAME_UNCISAL')
        db = DatabaseSession()
        session = db.get_session()
        try:
            nome = session.execute(select(Usuario.nome).where(Usuario.usuario == username)).scalar()
        except:
            session.rollback()
            traceback.print_exc()
            return None
        return nome
    
    @staticmethod
    def check_login_cookie():
        load_dotenv()
        SALT = os.getenv('COOKIE_SALT')
        CManager = CookieManager()
        username = CManager.get_cookie_manager().get('AUTH_USERNAME_UNCISAL')
        if not username:
            return False
        hashed_cookie = hashlib.sha256(f'{username}:{SALT}'.encode()).hexdigest()
        cookie = CManager.get_cookie_manager().get('AUTH_COOKIE_UNCISAL')
        return hashed_cookie == cookie
            
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
                cookie = UsuarioService.create_login_cookie(user.usuario)
                CManager = CookieManager()
                CManager.get_cookie_manager().set('AUTH_COOKIE_UNCISAL', cookie, key='set-0')
                CManager.get_cookie_manager().set('AUTH_USERNAME_UNCISAL', user.usuario, key='set-1')
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
            
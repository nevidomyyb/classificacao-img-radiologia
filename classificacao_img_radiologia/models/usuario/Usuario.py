from sqlalchemy import Column, String, Integer, Boolean
from classificacao_img_radiologia.models.database import Base

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  
    nome = Column(String(100), nullable=False)
    matricula = Column(String(20), nullable=False, unique=True)
    usuario = Column(String(20), nullable=False, unique=True)
    senha = Column(String(150), nullable=False)
    curso = Column(String(50), nullable=False)
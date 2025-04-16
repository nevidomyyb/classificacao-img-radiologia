from sqlalchemy import Column, String, Integer, Boolean, DateTime, func
try:
    from classificacao_img_radiologia.models.database import Base
except:
    from models.database import Base


class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True, autoincrement=True)  
    nome = Column(String(100), nullable=False)
    matricula = Column(String(20), nullable=True, unique=True)
    usuario = Column(String(20), nullable=False, unique=True)
    senha = Column(String(150), nullable=False)
    curso = Column(String(50), nullable=True)
    dtcriado = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    
    email = Column(String(180), nullable=False, unique=True)
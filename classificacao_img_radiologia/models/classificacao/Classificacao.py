import os

from sqlalchemy import Column, String, Integer, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import validates, relationship
from models.database import Base
from utils.get_base_folder import get_media_folder

class Classificacao(Base):
    __tablename__ = 'classificacao'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    classificacao = Column(String(50), nullable=False)
    genero = Column(String(1), nullable=False)
    dtcadastro = Column(DateTime(timezone=True), default=func.now())
    dtnascimento_paciente = Column(Date, nullable=False)
    dtprocedimento = Column(DateTime(timezone=True), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    
    imagens = relationship('Imagem', lazy='immediate')
    @validates('classificacao')
    def validate_classifacao(self, key, value):
        valid = ['Normal', 'Com alteração']
        
        if value not in valid:
            raise ValueError('Classificação não permitida.')
        return value
    
    
        
    @property
    def media_folder(self):
        return os.path.join(get_media_folder(), f'user-{self.usuario_id}-classificacao-{self.id}')
        
    
    
    
    
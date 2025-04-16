from sqlalchemy import Column, String, Integer, DateTime, func, Date, ForeignKey
from sqlalchemy.orm import validates
from models.database import Base

class Classificacao(Base):
    __tablename__ = 'classificacao'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    classificacao = Column(String(50), nullable=False)
    genero = Column(String(1), nullable=False)
    dtcadastro = Column(DateTime(timezone=True), default=func.now())
    dtnascimento_paciente = Column(Date, nullable=False)
    dtprocedimento = Column(DateTime(timezone=True), nullable=False)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    
    
    @validates('classificacao')
    def validate_classifacao(self, key, value):
        valid = ['Normal', 'Com alteração']
        
        if value not in valid:
            raise ValueError('Classificação não permitida.')
        return value
    
    
        
        
        
    
    
    
    
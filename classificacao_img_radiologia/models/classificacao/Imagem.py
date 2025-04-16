from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, Date, ForeignKey
from models.database import Base

class Imagem(Base):
    __tablename__ = 'imagem'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    imagem_full_path = Column(String(524), nullable=False)
    classificacao_id = Column(Integer, ForeignKey('classificacao.id'), nullable=False)


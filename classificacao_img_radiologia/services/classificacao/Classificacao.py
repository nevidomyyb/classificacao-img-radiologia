from db import DatabaseSession
from models import Classificacao, Imagem
from sqlalchemy import or_, select
from utils.get_base_folder import get_media_folder

import os
import traceback


class ClassificacaoService:
    
    @staticmethod
    def register(classificacao:str, genero:str, dtnascimento_paciente: str, dtprocedimento:str, imagens:list, usuario_id: int, session=None) -> list:
        
        MEDIA_FOLDER = get_media_folder()
        
        if not session:
            db = DatabaseSession()
            session = db.get_session()
        
        try:
            classificacao = Classificacao(
                classificacao=classificacao,
                genero=genero,
                dtnascimento_paciente=dtnascimento_paciente,
                dtprocedimento=dtprocedimento,
                usuario_id=usuario_id
            )
            session.add(classificacao)
            session.commit()
            session.flush()
            class_media_folder = os.path.join(MEDIA_FOLDER, f'user-{str(usuario_id)}-classificacao-{str(classificacao.id)}')
            os.makedirs(MEDIA_FOLDER, exist_ok=True)
            os.makedirs(class_media_folder, exist_ok=True)
            for image in imagens:
                save_path = os.path.join(class_media_folder, image.name)
                with open(save_path, 'wb') as f:
                    f.write(image.getvalue())
                imagem_ = Imagem(
                    imagem_full_path=save_path,
                    classificacao_id=classificacao.id,   
                )
                session.add(imagem_)
                session.commit()
            return True, classificacao.id, len(imagens)
        except Exception as e:
            traceback.print_exc()
            session.rollback()
            return False, str(e), None
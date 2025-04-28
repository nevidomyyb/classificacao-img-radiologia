from db import DatabaseSession
from models import Classificacao, Imagem
from sqlalchemy import or_, select, func
from utils.get_base_folder import get_media_folder

import os
import traceback
import shutil

class ClassificacaoService:
    
    @staticmethod
    def delete_classification(class_id, _session=None):
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        try:
            classification = _session.scalar(select(Classificacao).where(Classificacao.id == class_id))
            path_to_delete = classification.media_folder
            if os.path.exists(path_to_delete):
                shutil.rmtree(path_to_delete)
            for img_instance in classification.imagens:
                _session.delete(img_instance)
            _session.delete(classification)
            _session.commit()
            return True, "Classificação deletada com sucesso."
        except  Exception as e:
            traceback.print_exc()
            return False, str(e)
    
    @staticmethod
    def save_classification(class_dict: dict, class_id: int, _session=None):
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        try:
            classification = _session.scalar(select(Classificacao).where(Classificacao.id == class_id))
            classification.classificacao = class_dict['classificacao']
            classification.genero = class_dict['genero']
            classification.dtnascimento_paciente = class_dict['dtnascimento_paciente']
            classification.dtprocedimento = class_dict['dtprocedimento']
            _session.commit()
            return True, "Classificação atualizada com sucesso."
        except Exception as e:
            traceback.print_exc()
            _session.rollback()
            return False, str(e)
            
    @staticmethod
    def get_classifications(user_id:int, is_admin:bool, page:int=1, _session=None)->tuple[bool, list[Classificacao], int]:
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        
        try:
            stmt = select(Classificacao)
            if not is_admin:
                stmt = stmt.where(Classificacao.usuario_id == user_id)
            stmt = stmt.order_by(Classificacao.dtcadastro.desc()).limit(10).offset((page-1)*10)
            result = _session.execute(stmt).scalars().all()
            total = _session.scalar(select(func.count(Classificacao.id)))
            return True, result, total
        except Exception as e:
            traceback.print_exc()
            return False, str(e), None
    @staticmethod
    def add_image_to_register(class_id, imagens: list, user_id:int, _session=None) -> list[bool, str]:
        MEDIA_FOLDER = get_media_folder()
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        
        try:
            classificacao = _session.scalar(select(Classificacao).where(Classificacao.id == class_id))
            class_media_folder = os.path.join(MEDIA_FOLDER, f'user-{str(user_id)}-classificacao-{str(classificacao.id)}')
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
                _session.add(imagem_)
            _session.commit()
            return True, 'Imagens registradas com sucesso.'
        except Exception as e:
            traceback.print_exc()
            _session.rollback()
            return False, str(e)         

    @staticmethod
    def delete_image_from_register(class_id:int, image_path=str,_session=None) -> list[bool, str]:
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        
        try:
            classificacao = _session.scalar(select(Classificacao).where(Classificacao.id == class_id))
            image_to_delete = _session.scalar(select(Imagem).where(Imagem.imagem_full_path==image_path))
            if not image_to_delete:
                return False, "Imagem não encontrada."
            classificacao.imagens.remove(image_to_delete)
            if os.path.exists(image_to_delete.imagem_full_path):
                os.remove(image_to_delete.imagem_full_path)
                _session.delete(image_to_delete)
                _session.commit()
                return True, 'Imagem excluida com sucesso.'
            return False, 'Algo ocorreu, imagem não excluida.'
        except Exception as e:
            traceback.print_exc()
            _session.rollback()
            return False, str(e),
    
    @staticmethod
    def register(classificacao:str, genero:str, dtnascimento_paciente: str, dtprocedimento:str, imagens:list, usuario_id: int, _session=None) -> list:
        
        MEDIA_FOLDER = get_media_folder()
        
        if not _session:
            db = DatabaseSession()
            _session = db.get_session()
        
        try:
            classificacao = Classificacao(
                classificacao=classificacao,
                genero=genero,
                dtnascimento_paciente=dtnascimento_paciente,
                dtprocedimento=dtprocedimento,
                usuario_id=usuario_id
            )
            _session.add(classificacao)
            _session.commit()
            _session.flush()
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
                _session.add(imagem_)
                _session.commit()
            return True, classificacao.id, len(imagens)
        except Exception as e:
            traceback.print_exc()
            _session.rollback()
            return False, str(e), None
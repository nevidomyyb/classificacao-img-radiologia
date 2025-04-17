import streamlit as st
import datetime

from models import Classificacao, Imagem
from partials.BasePage import BasePage
from services.usuario.Usuario import UsuarioService
from services.classificacao.Classificacao import ClassificacaoService
from math import ceil

class ListagemClassificacao(BasePage):
    def __init__(self):
        super().__init__("Listagem de Classificações", '', 'wide', 'collapsed', image=False)    
        st.session_state['page'] = 'Listagem de Classificações'
    
    def draw_list_with_pagination(self):
        if 'delete_info' in st.session_state:
            st.success(st.session_state['delete_info'])
            del st.session_state['delete_info']
        if 'page_classificacao' not in st.session_state:
            st.session_state['page_classificacao'] = 1
        success, classifications, total = ClassificacaoService.get_classifications(self.user.id, self.user.is_admin, st.session_state['page_classificacao'])
        if not success:
            st.error(classifications)
            return
        pages = ceil(total/10)
        _, col1, col2, col3 = st.columns([5, 1, 1, 1], gap='small')
        if col1.button("", icon=":material/chevron_left:", disabled=st.session_state['page_classificacao'] == 1):
            st.session_state['page_classificacao'] -= 1
            st.rerun()
        if col2.button("", icon=":material/chevron_right:", disabled=st.session_state['page_classificacao'] >= pages):
            st.session_state['page_classificacao'] += 1
            st.rerun()
        pages_list = [1] if total <= 10 else [i for i in range(1, pages+1)]
        st.session_state['page_classificacao'] = col3.selectbox(
            'Página',
            pages_list,
            index=pages_list.index(st.session_state['page_classificacao']),
            key='page_classificacao_select',
            label_visibility='collapsed',
            help='Selecione a página que deseja visualizar',
        )
        with st.container(border=True):
            cols = st.columns([1, 1, 1, 1, 1], gap='small')
            headers = ["Classificação", "Q° Imagens", "Data do Procedimento", "Data de Nascimento", "Gênero"]
            for i, col in enumerate(cols):
                col.markdown(f"##### {headers[i]}")
            st.divider()
            for classificacao in classifications:
                cols = st.columns([1, 1, 1, 1, 1], gap='small')
                cols[0].button(classificacao.classificacao, key=f'btn_classificacao_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                cols[1].button(str(len(classificacao.imagens)), key=f'btn_imagens_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                if isinstance(classificacao.dtprocedimento, datetime.datetime):
                    cols[2].button(classificacao.dtprocedimento.strftime('%d/%m/%Y'), key=f'btn_dtprocedimento_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                else:
                    cols[2].button('-----', key=f'btn_dtprocedimento_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                if isinstance(classificacao.dtnascimento_paciente, datetime.date):
                    cols[3].button(classificacao.dtnascimento_paciente.strftime('%d/%m/%Y'), key=f'btn_dtnascimento_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                else:
                    cols[3].button('-----', key=f'btn_dtnascimento_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
                cols[4].button(classificacao.genero, key=f'btn_genero_{classificacao.id}',on_click=self.show_classification, args=(classificacao,), type='tertiary')
    
    @st.fragment
    @st.dialog("Classificação", width='large')
    def show_classification(self, classificacao: Classificacao):
        imagens = classificacao.imagens
        if 'curr' not in st.session_state:
            st.session_state.curr = 0
        with st.container(border=True):
            col1, col2 = st.columns([1, 1],gap='large')
            if col1.button("", icon=":material/chevron_left:"):
                if st.session_state.curr > 0:
                    st.session_state.curr -= 1
            if col2.button("", icon=":material/chevron_right:"):
                if st.session_state.curr < len(imagens) - 1:
                    st.session_state.curr += 1
            current_img = imagens[st.session_state.curr]
            st.image(current_img.imagem_full_path, )
        _classificacao = st.selectbox(
            "Classificação",
            ["Normal", "Com alteração"],
            index=["Normal", "Com alteração"].index(classificacao.classificacao),
            help='Selecione uma opção.',
        )
        genres = [{"value": "M", "label": "Masculino"}, {"value": "F", "label": "Feminino"}]
        genero = st.selectbox('Gênero', genres, index=0 if classificacao.genero == "M" else 1, placeholder='Selecione uma opção', format_func=lambda x : x['label'])
        dtnascimento_pasciente = st.date_input('Data de Nascimento do Paciente', value=classificacao.dtnascimento_paciente, format="DD/MM/YYYY")
        dtprocedimento = st.date_input('Data do Procedimento', value=classificacao.dtprocedimento, format='DD/MM/YYYY')
        col1, _, _, _, col2 = st.columns([1, 1, 1, 1, 1])
        if col1.button("Salvar"):
            class_dict = {
                'classificacao': _classificacao,
                'genero': genero['value'],
                'dtnascimento_paciente': dtnascimento_pasciente,
                'dtprocedimento': dtprocedimento
            }
            success, msg = ClassificacaoService.save_classification(class_dict=class_dict, class_id=classificacao.id)
            if success:
                st.success(msg)
            else:
                st.error(msg)
        if col2.button("Excluir", type='secondary', icon=':material/delete:'):
            success, msg = ClassificacaoService.delete_classification(classificacao.id)
            if success:
                st.session_state.delete_info = msg
                st.rerun()
            else:
                st.error(msg)
            
    
    def draw(self):
        isAuthenticated = UsuarioService.check_login_cookie()
        if not isAuthenticated:
            st.switch_page('main.py')
        self.draw_list_with_pagination()
    
import streamlit as st

from partials.BasePage import BasePage
from services.usuario.Usuario import UsuarioService
from services.classificacao.Classificacao import ClassificacaoService

class Classificacao(BasePage):
    def __init__(self):
        super().__init__("Registro de Classificação", '', 'centered', 'collapsed')    
        st.session_state['page'] = 'Registro de Classificação'
    
    def _register_classificacao(self, usuario_id: int):
        success, classificacao_id, n_imagens = ClassificacaoService.register(
            self.classifcacao,
            self.genero,
            self.dtnascimento_paciente,
            self.dtprocedimento,
            self.imagems,
            usuario_id,
        )
        return success, classificacao_id, n_imagens
    
    def draw(self):
        isAuthenticated = UsuarioService.check_login_cookie()
        user_id = UsuarioService.get_user_id_by_cookie()
        if not isAuthenticated:
            st.switch_page('main.py')
        with st.container(border=True):
            
            options  = ['Normal', 'Com alteração']
            genres = ['M', 'F']
            self.imagems = st.file_uploader("Enviar Imagem", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True, )
            self.classifcacao = st.selectbox('Classificação', options, index=None, placeholder='Selecione uma opção')
            self.genero = st.selectbox('Gênero', genres, index=None, placeholder='Selecione uma opção')
            self.dtnascimento_paciente = st.date_input('Data de Nascimento do Paciente', value=None, format="DD/MM/YYYY")
            self.dtprocedimento = st.date_input('Data do Procedimento', value=None, format='DD/MM/YYYY')
            
            if st.button(
                'Registrar', disabled= not self.imagems or \
                    not self.classifcacao or \
                    not self.genero or \
                    not self.dtnascimento_paciente or \
                    not self.dtprocedimento,
            ):
                success, classificacao_id, n_imagens = self._register_classificacao(user_id)
                if success is True:
                    st.success(f'Classificação registrada com sucesso! ID: {classificacao_id} ({n_imagens} imagens)')
                else:
                    st.error(f'Erro ao registrar classificação: {classificacao_id}')
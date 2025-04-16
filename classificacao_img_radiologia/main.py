import streamlit as st

from services.usuario.Usuario import UsuarioService
from partials.BasePage import BasePage
from streamlit import switch_page

class Main(BasePage):
    def __init__(self):
        super().__init__('Login', '🔑', 'centered')
        st.session_state['page'] = 'login'
        
    def draw(self):
        isAuthenticated = UsuarioService.check_login_cookie()
        if isAuthenticated:
            switch_page('pages/register_classifcacao.py')
            
        with st.container(border=True):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            c1, _, _, c2 = st.columns([1, 2, 2, 1])
            if c1.button('Entrar', disabled=not usuario or not senha):
                #Logica para checar senha
                response = UsuarioService.login(usuario,senha)
                if response[0] is True:
                    switch_page('pages/register_classifcacao.py')
                else:
                    st.info(response[1])
            if c2.button('Registrar'):
                #Go to tela de registro
                switch_page('pages/register_user.py')
if __name__ == "__main__":
    main = Main()
    main.mount()
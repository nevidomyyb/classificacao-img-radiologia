import streamlit as st
from partials.Bottom import Bottom
from services.usuario.Usuario import UsuarioService

class BasePage(Bottom):
    
    def __init__(self, title: str, icon: str, layout: str, sidebar_state: str=None, image: bool=True):
        self.image = image
        try:
            st.set_page_config(page_title=title, page_icon=icon, layout=layout, initial_sidebar_state=sidebar_state)
        except Exception as e:
            ...
    
    def mount(self, ):
        isAuthenticated = UsuarioService.check_login_cookie()
        if isAuthenticated:
            nome_completo, self.user = UsuarioService.get_name_from_cookie(return_user=True)
            col1, _, col3, col4 = st.columns([1, 1, 1, 1])
            col1.caption(f"Olá, {nome_completo}")
            if col4.button("Logout", use_container_width=True):
                UsuarioService.logout()
            if st.session_state['page'] == 'Registro de Classificação':
                if col3.button("Registros", use_container_width=True):
                    st.switch_page("pages/list_classificacao.py")
            elif st.session_state['page'] == 'Listagem de Classificações':
                if col3.button("Registrar", use_container_width=True):
                    st.switch_page('pages/register_classifcacao.py')

        _, col, _ = st.columns([1, 1, 1])
        if self.image:
            col.image('classificacao_img_radiologia/assets/UNCISAL.png', width=200)
        self.draw()
        self.draw_bottom()
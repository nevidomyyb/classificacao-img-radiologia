import streamlit as st
from partials.BasePage import BasePage

class Main(BasePage):
    def __init__(self):
        super().__init__('Login', '🔑', 'centered')
        st.session_state['page'] = 'login'
        
    def draw(self):
        _, col, _ = st.columns([1, 1, 1])
        col.image('classificacao_img_radiologia/assets/UNCISAL.png', width=200)
        with st.container(border=True):
            usuario = st.text_input("Usuário", placeholder="Digite seu usuário")
            senha = st.text_input("Senha", type="password", placeholder="Digite sua senha")
            if st.button('Entrar', disabled=not usuario or not senha):
                st.success("Sucesso")
            
if __name__ == "__main__":
    main = Main()
    main.mount()
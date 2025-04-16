import streamlit as st
from partials.Bottom import Bottom
class BasePage(Bottom):
    
    def __init__(self, title: str, icon: str, layout: str, sidebar_state: str=None):
        try:
            st.set_page_config(page_title=title, page_icon=icon, layout=layout, initial_sidebar_state=sidebar_state)
        except Exception as e:
            ...
    
    def mount(self, ):
        _, col, _ = st.columns([1, 1, 1])
        col.image('classificacao_img_radiologia/assets/UNCISAL.png', width=200)
        self.draw()
        self.draw_bottom()
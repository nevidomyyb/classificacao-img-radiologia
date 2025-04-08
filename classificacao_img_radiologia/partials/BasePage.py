import streamlit as st

class BasePage():
    
    def __init__(self, title: str, icon: str, layout: str, sidebar_state: str=None):
        try:
            st.set_page_config(page_title=title, page_icon=icon, layout=layout, initial_sidebar_state=sidebar_state)
        except Exception as e:
            ...
    
    def mount(self, ):
        self.draw()
import streamlit as st
from streamlit_extras.bottom_container import bottom

class Bottom:
    
    def create_link(destination: str, icon: str, text: str, col):
        col.html(
            f"""
            <a href="{destination}" class="custom-link" target="_blank">
                <img src="{icon}" alt="{text}"/> {text}
            </a>
            """
        )
    
    def draw_bottom(self, ):
        
        st.html(
            """
            <style>
                .custom-link {
                    text-decoration: none;
                    color: black;
                }
                .custom-link:hover {
                    text-decoration: underline; 
                    color: black; 
                }
            </style>
            """,
        )
        st.html(
            f"""
            <img src="https://img.icons8.com/?size=24&id=61343&format=png&color=000000">
            Desenvolvido por
            <a href="https://www.linkedin.com/in/pedro-cunha-nev/" class="custom-link" target="_blank">
                <img src="https://img.icons8.com/?size=24&id=85044&format=png&color=000000" alt="linkedin"/> Pedro Cunha
            </a>
            """
        )
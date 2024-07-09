import re
from time import sleep
import streamlit as st

st.title("Tais")

st.subheader("Tributo Devido")


def validar_email(email: str) -> bool:
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(regex, email):
        return True
    return False

def validar_telefone(telefone: str) -> bool:
    regex = r'^\+?[1-9]\d{1,14}$'
    if re.match(regex, telefone):
        return True
    return False

with st.form(key="form-login",clear_on_submit=True):

    email = st.text_input("Email")
    telefone = st.text_input("Telefone")

    login_button = st.form_submit_button("Login")

    if login_button:
        if validar_email(email) and validar_telefone(telefone):
            st.session_state['Email'] = email
            st.session_state['Login'] = 'Logado'
            st.success('Login realizado com sucesso!')
            sleep(2)
            st.switch_page('chat_app.py')
            
        else:
            st.error("Favor verificar os dados.")

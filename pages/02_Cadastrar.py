from time import sleep

import streamlit as st

from aux.func import valida_email, valida_telefone
from aux.queries import insert_user, verify_user
from aux.mod import User, token_limit_default

st.title("Tais")
st.write("Cadastrar para acessar chat")

with st.form(key="form-signin",clear_on_submit=True):
    email = st.text_input("Email")
    nome = st.text_input("Nome")
    telefone = st.text_input("Telefone")

    cadastrar_button = st.form_submit_button("Cadastrar")
    if cadastrar_button:
        if valida_email(email) and valida_telefone(telefone):
            ret = verify_user(email)
            if ret:
                st.warning('Email já cadastrado!')
            else:
                user = User(nome=nome, email=email, telefone=telefone, token_limit=token_limit_default)
                user = insert_user(user)
                st.session_state['Logged_User'] = user
                st.success('Login realizado com sucesso!')
                sleep(1)
                st.switch_page('./pages/03_Chat.py')
        else:
            st.error("Favor verificar os dados.")
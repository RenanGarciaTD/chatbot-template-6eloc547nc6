from time import sleep

import streamlit as st

from aux.func import valida_email
from aux.mod import User
from aux.queries import verify_user

st.title("Tais")
st.write("Acessar chat")

with st.form(key="form-login",clear_on_submit=True):
    email = st.text_input("Email")
    
    acessar_button = st.form_submit_button("Acessar")
    if acessar_button:    
        if valida_email(email):
            ret = verify_user(email)
            if ret:
                user = User(name=ret[1], telefone=ret[2], email=ret[3], token_limit=ret[4], token_used=ret[5])
                st.session_state['Logged_User'] = user
                st.success('Login realizado com sucesso!')
                sleep(1)
                st.switch_page('./pages/03_Chat.py')
            else:
                st.error('Email não encontrado')
        else:
            st.error('Verificar email inserido!')
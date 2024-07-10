import streamlit as st

st.set_page_config(page_title="Tais - Tributo Devido", page_icon="random", initial_sidebar_state="collapsed")

# with st.sidebar:
#     st.image("./media/logo_tributo.png")

st.subheader("Assistente inteligente desenvolvido pela Tributo Devido")
st.divider()
if st.button("Já possuo cadastro", key='bt_acessar'):
    st.switch_page('./pages/01_Acessar.py')
if st.button("Novo cadastro", key='bt_cadastrar'):
    st.switch_page('./pages/02_Cadastrar.py')
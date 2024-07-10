from time import sleep
import aux.rag_chat_lib as glib
import aux.db as db
from aux.queries import insert_question, update_feedback
from aux.mod import Question

import streamlit as st

try:
    user = st.session_state['Logged_User']
except:
    st.switch_page('main.py')

st.title("Tais Chatbot") #page title
st.markdown(f"Olá, {user.name}!")
st.progress((user.token_used/user.token_limit), text=f'Você já usou: {((user.token_used/user.token_limit)*100):,.2f} % dos tokens.')

if 'bt_feedback' not in st.session_state:
    st.session_state.bt_feedback = {}
def disable_button(button_id):
    st.session_state.bt_feedback[button_id] = True

if 'chat_history' not in st.session_state.keys():
    st.session_state.chat_history = [{'id': 0, 'role': 'assistant', 'text': 'Como posso te ajudar?'}]
    
if 'memory' not in st.session_state.keys(): #see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory() #initialize the memory

if 'vector_index' not in st.session_state.keys():
    st.session_state.vector_index = glib.get_index() 

# Disable text input when assistant is responding
if "disabled" not in st.session_state:
    st.session_state["disabled"] = False

# Toggle disabled state
def disable_toggle():
    st.session_state["disabled"] = not(st.session_state["disabled"])

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["text"])
        if message["role"] == 'assistant' and message["id"] != 0:
            texto_feedback, b_bom, b_ruim = st.columns([2,1,1])
            texto_feedback.markdown('Essa resposta foi boa?')
            if b_bom.button('👍', use_container_width=True, key=f'_{message["id"]}', args=(message["id"],), on_click=disable_button, disabled=st.session_state.bt_feedback[message["id"]]):
                update_feedback(True, message["id"])
            if b_ruim.button('👎', use_container_width=True, key=f'_{message["id"]}', args=(message["id"],), on_click=disable_button, disabled=st.session_state.bt_feedback[message["id"]]):
                update_feedback(True, message["id"])

input_text = st.chat_input("Qual sua pergunta?", disabled=st.session_state["disabled"])

if input_text:
    new_id = st.session_state.chat_history[-1]['id'] + 1
    with st.chat_message("user"):
        st.markdown(input_text)
        
    with st.chat_message("assistant"):
        with st.spinner("Trabalhando nisso..."):
            response_content = glib.get_rag_chat_response(input_text=input_text,
                                                            memory=st.session_state.memory,
                                                            index=st.session_state.vector_index) #call the model through the supporting library
            placeholder = st.empty()
            full_response = ''
            for item in response_content:
                full_response += item
                sleep(0.65)
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
            st.session_state.bt_feedback[new_id] = False

    st.session_state.chat_history.append({"id": new_id, "role": "user", "text": input_text})
    st.session_state.chat_history.append({"id": new_id, "role": "assistant", "text": response_content})
    question = insert_question(Question(user_id=user.id, session_id='0', question= input_text, answer=response_content, feedback=0, used_tokens=0))
    texto_feedback, b_bom, b_ruim = st.columns([2,1,1])
    texto_feedback.markdown('Essa resposta foi boa?')
    if b_bom.button('👍', use_container_width=True, key=f'_{message["id"]}', args=(message["id"],), on_click=disable_button, disabled=st.session_state.bt_feedback[new_id]):
        update_feedback(True, question)
    if b_ruim.button('👎', use_container_width=True, key=f'_{message["id"]}', args=(message["id"],), on_click=disable_button, disabled=st.session_state.bt_feedback[new_id]):
        update_feedback(True, question.id)
        

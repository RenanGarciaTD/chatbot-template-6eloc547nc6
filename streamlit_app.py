import streamlit as st
from openai import OpenAI

openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="RAG Chatbot") #HTML title
st.title("RAG Chatbot") #page title

if 'memory' not in st.session_state: #see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory() #initialize the memory

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'vector_index' not in st.session_state:
    st.session_state.vector_index = glib.get_index() 

#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"]) #display the chat content

input_text = st.text_area("Input text", label_visibility="collapsed") #display a multiline text box with no label
go_button = st.button("Go", type="primary") #display a primary button
if go_button: #code in this if block will be run when the button is clicked
    with st.chat_message("user"): #display a user chat message
        st.markdown(input_text) #renders the user's latest message

    with st.spinner("Working..."): #show a spinner while the code in this with block runs
        response_content = glib.get_rag_chat_response(input_text=input_text, memory=st.session_state.memory, index=st.session_state.vector_index) #call the model through the supporting library

        st.write(response_content) #display the response content
        st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
        st.session_state.chat_history.append({"role":"assistant", "text":response_content}) #append the bot's latest message to the chat history

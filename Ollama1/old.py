import streamlit as st
from config import Config
from helpers.llm_helper import chat, stream_parser

st.set_page_config(
    page_title=Config.PAGE_TITLE,
    initial_sidebar_state="expanded"
)

st.title(Config.PAGE_TITLE)

with st.sidebar:   
    st.markdown("# Chat Options")

    model = st.selectbox('What model would you like to use?', Config.OLLAMA_MODELS)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_prompt := st.chat_input("How can I help you"):
    with st.chat_message("user"):
        st.markdown(user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.spinner('Generating response...'):
        llm_stream = chat(user_prompt, model=model)
        stream_output = st.write_stream(stream_parser(llm_stream))
        st.session_state.messages.append({"role": "assistant", "content": stream_output})

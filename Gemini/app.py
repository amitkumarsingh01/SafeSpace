from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as gai
from PIL import Image

gai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = gai.GenerativeModel("gemini-1.5-flash-latest")
chat = model.start_chat(history=[])

def gemini_img_bot(input, image):
    if input != "":
        medical_prompt = f"Please analyze the following medical image and provide insights. Text input: {input}"
        response = chat.send_message([medical_prompt, image])
    else:
        medical_prompt = "Please analyze the following medical image."
        response = chat.send_message([medical_prompt, image])
    return response.text

def gemini_text_bot(question):
    if question == "":
        return "Please enter your medical query."
    
    medical_prompt = f"Please respond as a medical chatbot. Question: {question}"
    
    response = chat.send_message(medical_prompt)
    return response.text

if 'chats_pro' not in st.session_state:
    st.session_state['chats_pro'] = []

st.set_page_config(page_title="SafeSpace Image and Text Bot", page_icon="🤖")
st.header("SafeSpace Bot")

st.sidebar.markdown(
    """
    # Welcome to SafeSpace

    ### Give Text / Image input for medical queries.
    """
)

input_text = st.text_input("Enter Medical Query: ", key="input_text")
uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])
image = None

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Submit")

if submit:
    if input_text != "" and image is not None:
        rsp = gemini_img_bot(input_text, image)
        st.session_state['chats_pro'].append(("BOT", {"text": rsp}))
        st.session_state['chats_pro'].append(("YOU", {"text": input_text, "image": image}))
    elif input_text != "":
        rsp = gemini_text_bot(input_text)
        st.session_state['chats_pro'].append(("BOT", {"text": rsp}))
        st.session_state['chats_pro'].append(("YOU", {"text": input_text}))
    elif image is not None:
        rsp = gemini_img_bot("", image)
        st.session_state['chats_pro'].append(("BOT", {"text": rsp}))
        st.session_state['chats_pro'].append(("YOU", {"image": image}))

    st.subheader("Response: ")
    for i, (role, content) in enumerate(reversed(st.session_state['chats_pro'])):
        role_emoji = "👤" if role == "YOU" else "🤖"
        st.write(f"**{role_emoji} {role}:** {content['text']}")
        if "image" in content:
            st.image(content["image"], caption="Uploaded Image.", use_column_width=True)
        if (i + 1) % 2 == 0:
            st.write("")

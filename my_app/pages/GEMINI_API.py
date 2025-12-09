import streamlit as st
from google import genai

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
st.subheader("Gemini API")

#Initialise session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

#displaying existing messages
for message in st.session_state.messages:
    if message["role"] == "model" :
        role = "assistant"
    else:
        role = message["role"]
    with st.chat_message(role):
        st.markdown(message["parts"][0]["text"])

#user input
prompt = st.chat_input("Say something")

if prompt :
    #display user messages
    with st.chat_message("user"):
        st.markdown(prompt)

    #save user messages
    st.session_state.messages.append({
        "role": "user",
        "parts": [{"text": prompt}]
    })

    #Send to Gemini
    response = client.models.generate_content_stream(
        model="gemini-2.5-flash",
        contents=st.session_state.messages,
    )

    #Display streaming assistant output
    with st.chat_message("assistant"):
        container = st.empty()
        full_reply = ""
        for chunk in response:
            full_reply += chunk.text
            container.markdown(full_reply)

    #save assistant message
    st.session_state.messages.append(
        {"role": "model", "parts": [{"text": full_reply}]}
    )

    st.rerun()
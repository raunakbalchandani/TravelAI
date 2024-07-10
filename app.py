import streamlit as st
from backend1 import handle_query, get_chatgpt_response, detect_intent

st.title("Travel Agent Chatbot")

st.write("Welcome! Ask me about travel packages or general travel-related questions.")

query = st.text_input("Your question:")

if st.button("Submit"):
    if query:
        if detect_intent(query):
            response = handle_query(query)
        else:
            response = get_chatgpt_response(query)
        st.write(response)
    else:
        st.write("Please enter a question.")

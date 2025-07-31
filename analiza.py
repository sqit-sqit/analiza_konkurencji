# analiza.py

import os
import streamlit as st
from openai import OpenAI   
from dotenv import dotenv_values


env = dotenv_values(".env")

if not st.session_state.get("openai_api_key"):
    if os.environ.get('APP_ENV') != 'production':
        if "OPENAI_API_KEY" in env:
            st.session_state["openai_api_key"] = env["OPENAI_API_KEY"]
    elif os.environ.get("OPENAI_API_KEY"):
        st.session_state["openai_api_key"] = os.environ["OPENAI_API_KEY"]
    else:
        st.info("Dodaj swój klucz API OpenAI aby móc korzystać z tej aplikacji")
        st.session_state["openai_api_key"] = st.text_input("Klucz API", type="password")
        if st.session_state["openai_api_key"]:
            st.rerun()

if not st.session_state.get("openai_api_key"):
    st.stop()

api_key= st.session_state["openai_api_key"]
client = OpenAI(api_key=api_key)


def analizuj_oferte(prompt: str):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    return response.choices[0].message.content

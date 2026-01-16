# titulo
# input do chat (campo para o envio da menasgem)
# a cada mensagem que o usuario enviar:
# mostrar a mensagem que o usuario enviou no chat
# pegar a pergunta e enviar para um IA resposnder
# exibir a resposta da IA na tela

##Streamlit -> apenas com Python criar o front e o backend
## A IA que vamos usar: OpenAI
import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="ChatBot do João", page_icon="🤖")
st.write("# ChatBot do João")


modelo_ia = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"], base_url="https://api.groq.com/openai/v1"
)


if not "lista_mensagens" in st.session_state:
    st.session_state["lista_mensagens"] = []

texto_usuario = st.chat_input("Digite sua Mensagem")

for mensagem in st.session_state["lista_mensagens"]:
    role = mensagem["role"]
    content = mensagem["content"]
    st.chat_message(role).write(content)

if texto_usuario:
    st.chat_message("user").write(texto_usuario)
    mensagem_usuario = {"role": "user", "content": texto_usuario}
    st.session_state["lista_mensagens"].append(mensagem_usuario)

    resposta_ia = modelo_ia.chat.completions.create(
        messages=st.session_state["lista_mensagens"], model="llama-3.3-70b-versatile"
    )

    texto_resposta_ia = resposta_ia.choices[0].message.content

    st.chat_message("assistant").write(texto_resposta_ia)
    mensagem_ia = {"role": "assistant", "content": texto_resposta_ia}
    st.session_state["lista_mensagens"].append(mensagem_ia)

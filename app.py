import streamlit as st
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards

st.title("AI Flashcards for Tech Learners")
st.write("Insira um texto ou URL para gerar flashcards automáticos!")

# Escolha entre URL ou texto
input_type = st.radio("Escolha o tipo de entrada:", ("URL", "Texto"))
text = ""

if input_type == "URL":
    url = st.text_input("Insira o link do artigo:")
    if st.button("Gerar Flashcards") and url:
        text = extract_text_from_url(url)
        st.write("Texto extraído:", text[:500] + "...")  # Mostra um preview
elif input_type == "Texto":
    text = st.text_area("Cole o texto aqui:", height=200)
    if st.button("Gerar Flashcards") and text:
        pass  # Já temos o texto

# Gera e exibe flashcards
if text:
    flashcards = generate_flashcards(text)
    for i, card in enumerate(flashcards):
        with st.expander(f"Pergunta {i+1}: {card['Pergunta']}"):
            st.write(f"Resposta: {card['Resposta']}")
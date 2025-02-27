import streamlit as st
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards

st.title("AI Flashcards para Tech Learners")
st.write("Insira um texto ou URL para gerar flashcards automáticos com IA!")

# Escolha entre URL ou texto
input_type = st.radio("Escolha o tipo de entrada:", ("URL", "Texto"))
text = ""

if input_type == "URL":
    url = st.text_input("Insira o link do artigo:")
    if st.button("Gerar Flashcards") and url:
        text = extract_text_from_url(url)
        if not text.startswith("Erro"):
            st.write("Texto extraído:", text[:500] + "...")  # Preview do texto
        else:
            st.error(text)
elif input_type == "Texto":
    text = st.text_area("Cole o texto aqui:", height=200)
    if st.button("Gerar Flashcards") and text:
        st.write("Texto inserido:", text[:500] + "...")  # Preview opcional

# Gera e exibe flashcards
if text and not text.startswith("Erro"):
    with st.spinner("Gerando flashcards com IA..."):
        flashcards = generate_flashcards(text)
    if "Erro" not in flashcards[0]["Pergunta"]:
        st.success("Flashcards gerados com sucesso!")
        for i, card in enumerate(flashcards):
            with st.expander(f"Pergunta {i+1}: {card['Pergunta']}"):
                st.write(f"Resposta: {card['Resposta']}")
    else:
        st.error(flashcards[0]["Resposta"])
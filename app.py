import streamlit as st
from streamlit_tailwind import tailwind  # Importa a biblioteca
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards
from firebase_db import save_flashcards, get_flashcard_history

# Configuração inicial da página
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="AI Flashcards")

# Aplica Tailwind ao app inteiro (fundo geral)
tailwind("bg-gray-100 text-gray-800 font-roboto")

# Título com Tailwind
st.title("🎴 AI Flashcards para Tech Learners", className="text-gray-800 text-4xl")
st.write("Insira um texto ou URL para gerar flashcards automáticos com IA!", className="text-gray-700")

# Escolha entre URL ou texto
input_type = st.radio("Escolha o tipo de entrada:", ("URL", "Texto"), className="text-gray-700")
text = ""

if input_type == "URL":
    url = st.text_input("Insira o link do artigo:", className="border-2 border-blue-500 rounded-md text-lg")
    if st.button("Gerar Flashcards", className="bg-green-600 text-white rounded-md text-lg py-2 px-4 hover:bg-green-700") and url:
        text = extract_text_from_url(url)
        if not text.startswith("Erro"):
            st.write("Texto extraído:", text[:500] + "...", className="text-gray-700")
        else:
            st.error(text)
elif input_type == "Texto":
    text = st.text_area("Cole o texto aqui:", height=200, className="border-2 border-blue-500 rounded-md text-lg")
    if st.button("Gerar Flashcards", className="bg-green-600 text-white rounded-md text-lg py-2 px-4 hover:bg-green-700") and text:
        st.write("Texto inserido:", text[:500] + "...", className="text-gray-700")

# Gera e exibe flashcards em duas colunas
if text and not text.startswith("Erro"):
    with st.spinner("Gerando flashcards com IA..."):
        flashcards = generate_flashcards(text)
    if "Erro" not in flashcards[0]["Pergunta"]:
        st.success("Flashcards gerados com sucesso!", className="text-green-600")
        save_flashcards(text, flashcards)
        col1, col2 = st.columns(2)
        for i, card in enumerate(flashcards):
            with col1 if i % 2 == 0 else col2:
                with st.expander(
                    f"Pergunta {i+1}: {card['Pergunta']}",
                    className="bg-blue-100 border border-blue-500 rounded-lg shadow-md p-2.5 mb-2.5"
                ):
                    st.write(
                        f"Resposta: {card['Resposta']}",
                        className="text-gray-800"
                    )
    else:
        st.error(flashcards[0]["Resposta"])

# Sidebar com Tailwind
with st.sidebar:
    if st.button("Ver Histórico", className="bg-red-600 text-white rounded-md text-lg py-2 px-4 hover:bg-red-700"):
        history = get_flashcard_history()
        st.write("### Histórico de Flashcards", className="text-gray-100")
        for entry in history:
            with st.expander(
                f"Gerado em {entry['timestamp']}",
                className="bg-gray-600 text-white rounded-md mb-2"
            ):
                st.write(f"Texto: {entry['input_text'][:100]}...", className="text-gray-200")
                for i, card in enumerate(entry["flashcards"]):
                    st.write(
                        f"{i+1}. {card['Pergunta']} - {card['Resposta']}",
                        className="text-gray-200"
                    )
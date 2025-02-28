import streamlit as st
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards
from firebase_db import save_flashcards, get_flashcard_history

# Configuração inicial da página
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="AI Flashcards")

# Estilização com CSS
st.markdown("""
<style>
/* Fundo geral */
body {
    background-color: #f5f5f5;
    color: #333333;
    font-family: 'Roboto', sans-serif;
}

/* Título */
h1 {
    color: #2c3e50;
    font-size: 2.5em;
}

/* Expansores (flashcards) */
.stExpander {
    background-color: #e6f3ff;
    border: 1px solid #3498db;
    border-radius: 10px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    padding: 10px;
    margin-bottom: 10px;
}
.stExpander summary {
    font-weight: bold;
    color: #2980b9;
}

/* Campos de entrada */
.stTextInput > div > input, .stTextArea > div > textarea {
    border: 2px solid #3498db;
    border-radius: 5px;
    font-size: 1.1em;
}

/* Botão de gerar flashcards */
.stButton > button {
    background-color: #025b8e;
    color: white;
    border-radius: 5px;
    font-size: 1.1em;
    padding: 8px 16px;
}
.stButton > button:hover {
    background-color: #347ba4;
}

/* Sidebar */
.css-1v0mbdj {  /* Classe do sidebar */
    background-color: #34495e;
    color: white;
}
.css-1v0mbdj h3 {
    color: #ecf0f1;
}
.css-1v0mbdj .stButton > button {
    background-color: #b3cddd;
}
.css-1v0mbdj .stButton > button:hover {
    background-color: #b3cddd;
}
</style>
""", unsafe_allow_html=True)

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
            st.write("Texto extraído:", text[:500] + "...")
        else:
            st.error(text)
elif input_type == "Texto":
    text = st.text_area("Cole o texto aqui:", height=200)
    if st.button("Gerar Flashcards") and text:
        st.write("Texto inserido:", text[:500] + "...")

# Gera e exibe flashcards em duas colunas
if text and not text.startswith("Erro"):
    with st.spinner("Gerando flashcards com IA..."):
        flashcards = generate_flashcards(text)
    if "Erro" not in flashcards[0]["Pergunta"]:
        st.success("Flashcards gerados com sucesso!")
        save_flashcards(text, flashcards)  # Salva no Firebase
        col1, col2 = st.columns(2)  # Divide em duas colunas
        for i, card in enumerate(flashcards):
            with col1 if i % 2 == 0 else col2:  # Alterna entre colunas
                with st.expander(f"Pergunta {i+1}: {card['Pergunta']}"):
                    st.write(f"Resposta: {card['Resposta']}")
    else:
        st.error(flashcards[0]["Resposta"])

# Histórico no sidebar
if st.sidebar.button("Ver Histórico"):
    history = get_flashcard_history()
    st.sidebar.write("### Histórico de Flashcards")
    for entry in history:
        with st.sidebar.expander(f"Gerado em {entry['timestamp']}"):
            st.write(f"Texto: {entry['input_text'][:100]}...")
            for i, card in enumerate(entry["flashcards"]):
                st.write(f"{i+1}. {card['Pergunta']} - {card['Resposta']}")
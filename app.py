import streamlit as st
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards
from firebase_db import save_flashcards, get_flashcard_history

# Configuração inicial da página
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="AI Flashcards")

# Estilização com CSS ajustada
st.markdown("""
<style>
body {
    background-color: #282828;
    color: #a0ced9;
    font-family: 'Courier New', monospace;
    background-image: linear-gradient(to bottom, #282828, #1a1a1a);
}

h1 {
    color: #40e0d0;
    font-size: 2.8em;
}

.stExpander {
    background-color: #b2dfdb;
    border: 1px solid #9370db;
    border-radius: 10px;
    box-shadow: 2px 2px 8px rgba(100, 65, 164, 0.3);
    padding: 12px;
    margin-bottom: 12px;
}
.stExpander summary {
    font-weight: bold;
    color: #6c3483;
}
.stExpander p, .stExpander div {
    color: #333;
}

.stTextInput > div > input, .stTextArea > div > textarea {
    border: 2px solid #40e0d0;
    border-radius: 5px;
    font-size: 1.1em;
    background-color: #1e1e1e;
    color: #a0ced9;
}

.stButton > button {
    background-color: #8ddad5;
    color: #1e1e1e;
    border-radius: 5px;
    font-size: 1.1em;
    padding: 10px 20px;
    border: none;
    box-shadow: 0 0 5px #8ddad5;
}
.stButton > button:hover {
    background-color: #7ac9c0;
    box-shadow: 0 0 10px #7ac9c0;
}

.css-1v0mbdj {
    background-color: #1a1a1a;
    color: #40e0d0;
    border-right: 2px solid #9370db;
}
.css-1v0mbdj h3 {
    color: #8ddad5;
}
.css-1v0mbdj .stButton > button {
    background-color: #9370db;
    color: #1e1e1e;
    box-shadow: 0 0 3px #9370db;
}
.css-1v0mbdj .stButton > button:hover {
    background-color: #805cb3;
    box-shadow: 0 0 8px #805cb3;
}

/* Removendo hover vermelho da fonte e ajustando outros hovers */
.stExpander summary:hover,
.stTextInput > div > input:hover,
.stTextArea > div > textarea:hover,
.css-1v0mbdj h3:hover {
    color: #66cdaa; /* Turquesa mais escuro no hover */
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
import streamlit as st
from scraper import extract_text_from_url
from flashcard_generator import generate_flashcards
from firebase_db import save_flashcards, get_flashcard_history, clear_flashcard_history

# Configuração inicial da página (sem tema)
st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_title="AI Flashcards")

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

# Sidebar com histórico e botão de apagar
with st.sidebar:
    if st.button("Ver Histórico"):
        history = get_flashcard_history()
        st.write("### Histórico de Flashcards", className="text-gray-100")
        for entry in history:
            st_tw(f"""
            <div class="bg-gray-600 text-white rounded-md mb-2 p-2">
                <p class="font-bold">Gerado em {entry['timestamp']}</p>
                <p class="text-gray-200">Texto: {entry['input_text'][:100]}...</p>
                <ul class="text-gray-200">
                    {''.join([f'<li>{i+1}. {card["Pergunta"]} - {card["Resposta"]}</li>' for i, card in enumerate(entry["flashcards"])])}>
                </ul>
            </div>
            """)
    
    # Botão para apagar histórico com confirmação
    if st.button("Apagar Histórico"):
        if st.sidebar.checkbox("Confirmar exclusão"):
            clear_flashcard_history()
            st.success("Histórico apagado com sucesso!")
        else:
            st.warning("Marque a caixa para confirmar!")
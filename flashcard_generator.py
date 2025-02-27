import google.generativeai as genai
from dotenv import load_dotenv
import os
import ast

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY não encontrada no .env ou ambiente")
genai.configure(api_key=API_KEY)

def generate_flashcards(text):
    prompt = (
        "Analise o texto abaixo e gere 5 flashcards no formato "
        "'Pergunta: [pergunta clara e específica] Resposta: [resposta curta, mas com detalhes úteis]' "
        "com base em conceitos-chave, evitando repetições. Retorne como uma lista de dicionários Python "
        "(ex.: [{'Pergunta': '...', 'Resposta': '...'}, ...]):\n\n" + text
    )
    
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        print("Resposta bruta do Gemini:", response.text)  # Debug
        
        # Remove marcações de Markdown, se presentes
        cleaned_response = response.text.strip()
        if cleaned_response.startswith("```python"):
            cleaned_response = cleaned_response.replace("```python", "").strip()
        if cleaned_response.endswith("```"):
            cleaned_response = cleaned_response.replace("```", "").strip()
        
        # Parseia a resposta limpa
        flashcards = ast.literal_eval(cleaned_response)
        return flashcards
    except Exception as e:
        print(f"Erro ao gerar flashcards: {e}")
        return [{"Pergunta": "Erro", "Resposta": f"Não foi possível gerar flashcards: {e}"}]
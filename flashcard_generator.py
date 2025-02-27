import google.generativeai as genai

# Configure a chave API (melhor armazenar em variável de ambiente, mas por agora direto)
API_KEY = "sua-chave-aqui"  # Substitua por sua chave real
genai.configure(api_key=API_KEY)

def generate_flashcards(text):
    # Prompt otimizado para o Gemini
    prompt = (
        "Analise o texto abaixo e gere 5 flashcards no formato "
        "'Pergunta: [pergunta clara e específica] Resposta: [resposta curta, mas com detalhes úteis]' "
        "com base em conceitos-chave, evitando repetições. Retorne como uma lista de dicionários Python "
        "(ex.: [{'Pergunta': '...', 'Resposta': '...'}, ...]):\n\n" + text
    )
    
    try:
        # Configura o modelo (usamos "gemini-1.5-pro", disponível no free tier)
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        
        # Converte a resposta em uma lista de dicionários
        # O Gemini pode retornar texto puro, então usamos ast.literal_eval para parsear
        import ast
        flashcards = ast.literal_eval(response.text.strip())
        return flashcards
    except Exception as e:
        print(f"Erro ao gerar flashcards: {e}")
        return [{"Pergunta": "Erro", "Resposta": f"Não foi possível gerar flashcards: {e}"}]
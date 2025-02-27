def generate_flashcards(text):
    # Prompt para o Gemini (você cola manualmente por enquanto)
    prompt = (
        "Analise o texto abaixo e gere 5 flashcards no formato "
        "'Pergunta: [pergunta clara e específica] Resposta: [resposta curta, mas com detalhes úteis]' "
        "com base em conceitos-chave, evitando repetições:\n\n" + text
    )
    # Simulação de retorno (substitua pelo resultado real do Gemini)
    flashcards = [
        {"Pergunta": "Exemplo: O que é X?", "Resposta": "X é uma coisa útil."},
        # Adicione mais 4 manualmente após testar no Gemini
    ]
    return flashcards
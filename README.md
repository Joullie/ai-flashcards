# AI Flashcards para Tech Learners

[![Licença](https://img.shields.io/badge/licença-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## Descrição

Este projeto é uma aplicação web construída com Streamlit que utiliza inteligência artificial (IA) para gerar flashcards automaticamente a partir de textos ou URLs. A ferramenta é ideal para estudantes de tecnologia que desejam revisar conceitos de forma eficiente, mas funciona com material escrito de formatos diversos.

## Funcionalidades

-   **Geração Automática de Flashcards:** Insira um texto ou URL e a IA gera flashcards com perguntas e respostas concisas.
-   **Interface Amigável:** Design moderno e intuitivo, com opções para entrada de texto ou URL.
-   **Histórico de Flashcards:** Acompanhe seu progresso com um histórico de flashcards gerados, salvo no Firebase.

## Tecnologias Utilizadas

-   **Streamlit:** Framework Python para criação de aplicativos web interativos.
-   **Google Generative AI (Gemini 1.5 Pro):** Modelo de linguagem para geração de flashcards.
-   **Firebase:** Banco de dados NoSQL para armazenar o histórico de flashcards.
-   **Python:** Linguagem de programação principal.
-   **python-dotenv:** Biblioteca para gerenciar variáveis de ambiente.
-   **Beautiful Soup:** Biblioteca para extrair texto de páginas web.
-   **Requests:** Biblioteca para fazer requisições HTTP.

## Pendente:

- Estilização adequada.

## Como Usar

1.  **Clone o Repositório:**

    ```bash
    git clone [https://github.com/seu-usuario/ai-flashcards.git](https://github.com/seu-usuario/ai-flashcards.git)
    cd ai-flashcards
    ```

2.  **Crie um Ambiente Virtual (Opcional, mas recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate # No Linux/macOS
    venv\Scripts\activate # No Windows
    ```

3.  **Instale as Dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as Variáveis de Ambiente:**

    * Crie um arquivo `.env` na raiz do projeto.
    * Adicione sua chave de API do Gemini e as configurações do Firebase:

        ```
        GEMINI_API_KEY=sua_chave_gemini
        FIREBASE_API_KEY=sua_chave_firebase
        FIREBASE_AUTH_DOMAIN=seu-projeto.firebaseapp.com
        FIREBASE_DATABASE_URL=[https://seu-projeto.firebaseio.com](https://seu-projeto.firebaseio.com)
        FIREBASE_PROJECT_ID=seu-projeto
        FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
        FIREBASE_MESSAGING_SENDER_ID=seu-sender-id
        FIREBASE_APP_ID=seu-app-id
        ```

5.  **Execute o Aplicativo:**

    ```bash
    streamlit run app.py
    ```

6.  **Acesse o Aplicativo:**

    * Abra o navegador e acesse o endereço exibido no terminal.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

-   [Joullie](https://github.com/Joullie)

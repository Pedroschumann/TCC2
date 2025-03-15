Autor: Pedro Schumann

Resumo das principais características do projeto:

==> Configurar Ambiente:
    -> Criar ambiente virtual no projeto:
        - python -m venv venv (Isso vai criar o ambiente virtual e a pasta "vend" na hierarquia do projeto com todas as bibliotecas)
    -> Entrar na máquina virtual:
        .\venv\Scripts\Activate
    -> Caso dê erro pra rodar o comando acima, rodar o seguinte comando:
        Set-ExecutionPolicy Unrestricted -Scope Process

    - pip install ollama
    - pip install langchain
    - pip install langchain-community
    - pip install langchain-ollama
    - pip install beautifulsoup4
    - pip install faiss-cpu
    - pip install -U langchain langchain-ollama


==> Utilização da LLM llama3.2:
    - Se trata de uma LLM open source, dessa forma, diferente da open ai, não é necessário de um token para uso.
    - Além disso, consequência da característica acima, pode ser usada para aplicações que contenham informações sigilosas, por conta de não ser necessário enviar esses dados a nenhum local.
    - Mais infos no link: https://ollama.com/library/llama3.2

    Comandos:
    - ollama run llama3.2

    -> baixar llama3.2:1b
    - ollama run llama3.2:1b


==> Uso de Ollama
    - Download para uso: https://ollama.com/download
    - Se trata de uma ferramenta que deve ser instalada na máquina, ela permite executar diversos tipos de LLMs, inclusive a llama3.2.
    - Página do ollama: https://ollama.com/search
    - Link GitHub com informações de instalação e comandos: https://github.com/ollama/ollama-python/blob/main/README.md
    - Executável salvo na pasta "recursos" dentro desse diretório.

    -> OllamaEmbeddings: https://python.langchain.com/api_reference/ollama/embeddings/langchain_ollama.embeddings.OllamaEmbeddings.html#langchain_ollama.embeddings.OllamaEmbeddings


==> langchain
    - site principal: https://www.langchain.com/


==> groq


==> Como executar:
    - rodar no cmd: ollama run llama3.2
    - rodar a classe ChatBot.py


==> RAG
    - Documentação da langchain: https://python.langchain.com/docs/tutorials/rag/
    - Carregar documentos: https://python.langchain.com/docs/concepts/document_loaders/


==> OpenAI
    - Link pra gerar API-keys: https://platform.openai.com/settings/proj_R7GdyiIHNaPNnxFtxWUkXNmP/api-keys


==> Modelos de embeddings
    -> Rank dos melhores modelos: https://huggingface.co/spaces/mteb/leaderboard
    - legal-embeddings-br -> https://github.com/fabiolobato/legal-embeddings-br/tree/main
    - gte-Qwen2-7B-instruct -> https://huggingface.co/Alibaba-NLP/gte-Qwen2-7B-instruct
    - mxbai-incorporar-grande -> https://ollama.com/library/mxbai-embed-large
        - ollama pull mxbai-embed-large
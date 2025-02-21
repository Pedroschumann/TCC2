Autor: Pedro Schumann

Resumo das principais características do projeto:

==> Utilização da LLM llama3.2:
    - Se trata de uma LLM open source, dessa forma, diferente da open ai, não é necessário de um token para uso.
    - Além disso, consequência da característica acima, pode ser usada para aplicações que contenham informações sigilosas, por conta de não ser necessário enviar esses dados a nenhum local.
    - Mais infos no link: https://ollama.com/library/llama3.2

    Comandos:
    - ollama run llama3.2

    Para instalar:
    - pip install ollama
    - pip install langchain
    - pip install --quiet --upgrade langchain-text-splitters langchain-community langgraph
    - pip install -qU langchain-core
    - pip install -qU langchain-ollama
    - pip install -qU "langchain[groq]"


==> Uso de Ollama
    - Se trata de uma ferramenta que deve ser instalada na máquina, ela permite executar diversos tipos de LLMs, inclusive a llama3.2.
    - Página do ollama: https://ollama.com/search
    - Link GitHub com informações de instalação e comandos: https://github.com/ollama/ollama-python/blob/main/README.md
    - Executável salvo na pasta "recursos" dentro desse diretório.

==> langchain
    - site principal: https://www.langchain.com/

==> groq

==> Como executar:
    - rodar no cmd: ollama run llama3.2
    - rodar a classe ChatBot.py

==> RAG
    - Documentação da langchain: https://python.langchain.com/docs/tutorials/rag/
    - Carregar documentos: https://python.langchain.com/docs/concepts/document_loaders/
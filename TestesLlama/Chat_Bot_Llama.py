from ollama import chat
from ollama import ChatResponse
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

embeddings = OllamaEmbeddings(model="llama3")
vector_store = InMemoryVectorStore(embeddings)

response: ChatResponse = chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': 'Me informe como adicionar um RAG a sua pergunta',
  },
])
print(response['message']['content'])
# or access fields directly from the response object
print(response.message.content) 
import chromadb
client = chromadb.HttpClient("localhost", 8000)
#client = chromadb.PersistentClient()

collection_name = 'bgb-rag-prod'
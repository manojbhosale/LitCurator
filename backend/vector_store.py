# added this code to get the file name and page number
import chromadb
from sentence_transformers import SentenceTransformer

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("research_papers")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def store_documents(text_chunks):
    for i, chunk in enumerate(text_chunks):
        embedding = embedding_model.encode(chunk["text"]).tolist()
        collection.add(
            ids=[f"{chunk['file_name']}_pg{chunk['page']}"],
            embeddings=[embedding],
            metadatas=[{
                "text": chunk["text"],
                "page": chunk["page"],
                "file_name": chunk["file_name"]
            }]
        )

def query_documents(query):
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(query_embeddings=query_embedding, n_results=5)

    references = []
    print("Result data ================>", results)
    for metadata in results["metadatas"]:
        references.append({
            "text": metadata[0]["text"],
            "page": metadata[0]["page"],
            "file_name": metadata[0]["file_name"]
        })
    
    return references

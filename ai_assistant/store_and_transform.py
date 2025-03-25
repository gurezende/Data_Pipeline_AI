# Sript to store the formatted flight data in ChromaDB
# Converts each flight record into an embedding
# Stores it in ChromaDB for fast retrieval

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
from utils import fetch_flight_data, format_flight_data

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vector_db")

# Load the embedding model ("all-MiniLM-L6-v2" is a small, fast, and effective model)
embedding_model = embedding_functions.DefaultEmbeddingFunction()

# Create a collection for storing flight data
collection = chroma_client.get_or_create_collection(name="flight_prices", embedding_function=embedding_model)

# Fetch flight data
flight_data = fetch_flight_data()

# Format data for vectorization
flight_texts = format_flight_data(flight_data)

# Another option to Load the embedding model
# embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# embeddings = embedding_model.encode(flight_texts).tolist()

# Store the embedding in ChromaDB
for i, text in enumerate(flight_texts):
    collection.upsert(
        ids=[str(i)],
        documents=[flight_texts[i]]
    )

print(f"Stored {len(flight_texts)} flight records in ChromaDB!")


def search_flights(query, top_k=3):
    """Retrieve relevant flights based on a natural language query."""
        
    # Search ChromaDB for similar embeddings
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results


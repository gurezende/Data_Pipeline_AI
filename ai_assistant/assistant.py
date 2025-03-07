# This script takes a user query, embeds it, and retrieves relevant flight details:

import os
import groq
import chromadb
from chromadb.utils import embedding_functions
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
from ai_assistant.utils import search_flights
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Initialize Groq API client
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vector_db")

# Create a collection for storing flight data
collection = chroma_client.get_collection(name="flight_prices")

# Load the embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# RAG: Retrieve results from the Flights DB
# Connect to your existing Chroma collection
vector_db = Chroma(
    collection_name="flight_prices",
    embedding_function=embedding_model,
    persist_directory="./vector_db"
)

# Groq Response Generator
def groq_response(query, agent_type):
    current_date = datetime.now().strftime('%d/%m/%Y')

    # Create a document retriever
    retriever = vector_db.as_retriever()
    result = vector_db.similarity_search(query, k=30)
    # result = retriever.invoke(query,k=30)

    context = (
            f"Use the data retrieved from the retriever to answer the user's question: {result} "
            f"You must answer the query analyzing the data and providing insights and suggesting ways to save money when buying a flight."
            "If there is a suggestion to save money, say 'Save Money:'. "
            "Be as brief as possible. Don't use information that is not in the data."
            "If you don't know the answer, say 'I don't know'"
        )
        # imagem = "laennder.png"

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"{context}\nQuery: {query}",
            }
        ],
        model="llama3-8b-8192",
    )
    return chat_completion.choices[0].message.content.strip()



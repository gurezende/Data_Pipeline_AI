# This script takes a user query, embeds it, and retrieves relevant flight details:

import os
import chromadb
from datetime import datetime
import numpy as np
from dotenv import load_dotenv
from utils import search_flights
from typing_extensions import TypedDict, List

# Langchain Packages
from langchain_chroma import Chroma
from langchain import hub
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate

import warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize GROQ chat model
llm = init_chat_model("llama3-8b-8192", model_provider="groq", api_key=GROQ_API_KEY)

# Initialize ChromaDB client
chroma_client = chromadb.PersistentClient(path="./vector_db")

# # Create a collection for storing flight data
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

# Define prompt for question-answering
prompt = ChatPromptTemplate([
    ("system", '''You are an experienced data analyst. Use the following pieces of retrieved context to answer the question.
     Analyze the data retrieved and provide analysis and insights.
     If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.
    Question: {question}
    Context: {context}
    Answer:'''),
    ("human", "Hello, how are you doing?"),
    ("ai", "I'm doing well, thanks!"),
    ("human", "{question}")
])

# prompt = hub.pull("rlm/rag-prompt")

# Define state (data & types) for application
class State(TypedDict):
    question: str
    context: List[Document]
    answer: str


# Define application steps
def retrieve(state: State):
    """
    Retrieve relevant documents from the vector store based on the question.

    Args:
        state: State dictionary with the question to retrieve documents for.

    Returns:
        State dictionary with the retrieved documents in the "context" key.
    """
    retrieved_docs = vector_db.similarity_search(state["question"])
    return {"context": retrieved_docs}


def generate(state: State):
    """
    Generate an answer based on the provided question and retrieved context.

    Args:
        state: A State dictionary containing the user's question and a list of retrieved documents as context.

    Returns:
        A dictionary with a single key "answer" containing the generated response from the language model.
    """

    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


# Compile our application into a single graph object. 
# In this case, we are just connecting the two steps into a single sequence.
graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()



# Example usage
response = graph.invoke({"question": "What are 4 the most popular routes from MCO to VCP?"})
print(response["answer"])


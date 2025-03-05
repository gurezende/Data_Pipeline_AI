# This script takes a user query and responds using SQLDatabase retriever

# Imports

# From Langchain Packages
from langchain_community.utilities import SQLDatabase
from langchain.chat_models import init_chat_model
from langchain import hub
from langchain_community.tools.sql_database.tool import QuerySQLDatabaseTool
from langgraph.graph import START, StateGraph

# From Python Standard Library
import os
from dotenv import load_dotenv
from typing_extensions import TypedDict, Annotated
import warnings
warnings.filterwarnings("ignore")

# Load environment variables
load_dotenv()

# PostgreSQL connection details
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = "localhost"
DB_PORT = "5432"  # Default PostgreSQL port
DB_NAME = os.getenv("DB_NAME")

# Construct the PostgreSQL URI
postgres_uri = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Connect to the PostgreSQL database
db = SQLDatabase.from_uri(postgres_uri, schema="public", view_support=True, include_tables=['silver_flights'])

# The LangGraph state of our application controls what data is input to the application, transferred between steps, and output by the application.
class State(TypedDict):
    question: str
    query: str
    result: str
    answer: str

# Get Groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize GROQ chat model
llm = init_chat_model("llama3-8b-8192", model_provider="groq", api_key=GROQ_API_KEY)

# Pulling a prompt from the Prompt Hub to instruct the model.
# The prompt includes several parameters we will need to populate, such as the SQL dialect and table schemas
query_prompt_template = hub.pull("langchain-ai/sql-query-system-prompt")



class QueryOutput(TypedDict):
    """Defines a dictionary type called QueryOutput with a string value associated with the key query. 
    The Annotated type hint adds a descriptive note ("Syntactically valid SQL query.") to the query field"""

    # Annotated allows you to add type hints.
    query: Annotated[str, ..., "Successfully "]


# Class to generate SQL query, execute query through LLM, and generate answer
class SQLChain:
    
    def write_query(self, state: State):
        """Generate SQL query to fetch information."""
        prompt = query_prompt_template.invoke(
            {
                "dialect": db.dialect,
                "top_k": 10,
                "table_info": db.get_table_info(),
                "input": state["question"],
            }
        )

        # Request LLM to generate SQL query
        structured_llm = llm.with_structured_output(QueryOutput)
        result = structured_llm.invoke(prompt)
        return {"query": result["query"]}


    def execute_query(self, state: State):
        """Execute SQL query."""
        execute_query_tool = QuerySQLDatabaseTool(db=db)
        return {"result": execute_query_tool.invoke(state["query"])}


    def generate_answer(self, state: State):
        f"""Answer question using retrieved information as context.
            When the user asks for the price of a flight, let them know the price is in BRL."""
        prompt = (
            "Given the following user question, corresponding SQL query, "
            "and SQL result, answer the user question.\n\n"
            f'Question: {state["question"]}\n'
            f'SQL Query: {state["query"]}\n'
            f'SQL Result: {state["result"]}'
        )

        # Request LLM to generate answer
        response = llm.invoke(prompt)
        return {"answer": response.content}
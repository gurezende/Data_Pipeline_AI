# Web Application: 
# This app is intended to retrieve fligh tickets prices from the following flight companies and add to a postgres DB.
# Azul Airlines


# Import functions
from updatedb.updatedb import update_db
from ai_assistant.assistant import groq_response
from ai_assistant.assistant2 import SQLChain, State

# Imports
import streamlit as st
import pandas as pd
from updatedb.data_contract import Schema
from pandera.errors import SchemaError
from langgraph.graph import StateGraph, START

# bugfix for this problem
# Tried to instantiate class 'path.path’, but it does not exist! Ensure that it is registered via torch::class
import torch
torch.classes.__path__ = []

# Get BRL to USD conversion rate
from forex_converter import get_usd_rate
rate = get_usd_rate()

# Page title
st.set_page_config(page_title='Flight Prices Assistant',
                   page_icon=':airplane:', 
                   layout='wide',
                   initial_sidebar_state='collapsed')


# ------------------------ SIDEBAR   -------------------------
# Sidebar to configure the flights search to update the DB
with st.sidebar:

    # Section Title
    st.write('Update DB :minidisc:')

    days_ahead = st.multiselect('Number of days ahead',
                        options=[10, 30, 60, 90],
                        placeholder='Search flights N days ahead',
                        default=[10,30]
                    )
    
    origin_cd = st.text_input('Origin city code',
                              placeholder='Enter city code',
                              value='ZFF'
                              )
    
    destin_cd = st.text_input('Destination city code',
                              placeholder='Enter city code',
                              value='VCP'
                              )



    # Button to update the DB
    if st.button('Update DB'):
        for d in days_ahead:
            update_db(d, origin_cd, destin_cd)
        st.success('Database updated!')


#----------------------  MAIN PAGE  ----------------------

# Page Title
st.subheader(":gray[Welcome to the Flights AI Assistant]")

col1, _, _ = st.columns(3)
# Select an AI Assistant
with col1:
    assistant = st.pills('Select an AI Assistant', 
                            selection_mode='single',
                            options=['SQL Assistant', 'Flight Analyst']) 

st.divider()

#----------------------  SQL ASSISTANT  ----------------------

# If SQL Assistant is selected
if assistant == 'SQL Assistant':
    # Page Title
    st.title(':airplane_departure: :small_blue_diamond: FlightDB SQL Assistant :small_blue_diamond: :bar_chart:')
    st.write('This app is intended to retrieve information from the Postgres DB with Flights using Natural Language Processing via LLM assistant.')

    question = st.text_input('Ask a question',
                             placeholder='What are the most popular flights and times')

    # Instantiating SQLChain class
    sql_chain = SQLChain()

    # Orchestrating with LangGraph
    # Compile our application into a single graph object. 
    # In this case, we are just connecting the three steps into a single sequence.
    graph_builder = StateGraph(State).add_sequence(
        [sql_chain.write_query, sql_chain.execute_query, sql_chain.generate_answer]
    )

    # Take the graph that has been defined using the graph builder and turn it into an executable graph object for LLM
    graph_builder.add_edge(START, "write_query")
    graph = graph_builder.compile()

    # Run the graph

    if st.button('Run'):
        result = graph.invoke( {"question": question}, stream_mode="values" )
        # Response
        st.write(":green[-> Answer:]")
        st.write(result['answer'])
        # SQL Query generated
        st.write(":gray[-> SQL Query generated:]")
        st.code(result['query'], language='sql', wrap_lines=True) #sql_query



#----------------------  FLIGHT ANALYST  ----------------------

if assistant == 'Flight Analyst':
    # Page Title
    st.title(':airplane_departure: :small_blue_diamond: FlightDB Analyst :small_blue_diamond: :bar_chart:')
    st.write('This app is intended to analyze the information from the Postgres DB with Flights by an LLM assistant.')

    question = st.text_input('Ask a question',
                             placeholder='What are the most popular flights and times')
    
    if st.button('Run'):
        result = groq_response(query=question)
    
        # Response
        st.write(result)

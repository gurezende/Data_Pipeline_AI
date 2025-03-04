# Web Application: 
# This app is intended to retrieve fligh tickets prices from the following flight companies and add to a postgres DB.
# Azul Airlines


# Import functions
from updatedb import update_db

# Imports
import streamlit as st
import pandas as pd
from data_contract import Schema
from pandera.errors import SchemaError


# Page title
st.set_page_config(page_title='Flight Prices Assistant',
                   page_icon=':airplane:', 
                   layout='wide',
                   initial_sidebar_state='expanded')

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
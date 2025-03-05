# '''This script is to load the flights data to a Postgres Database.'''

# Imports
import pandas as pd
from updatedb.data_contract import validate_data
import streamlit as st

# SQLAlchemy imports
from updatedb.database import engine #import engine

def load_to_sql(flight_date:str, file_path = './data/flights.csv'):
  '''
  Load table to SQL database
  - Inputs:
  * file path: str = path to the csv table with flight fares
  * flight_date: str = search date for the flight
   '''
  # Data
  df = pd.read_csv(file_path)

  # Format date
  yr = flight_date[-4:] #get year => last 4 digits of the flight date
  df['dt'] = (
      df
      .dt
      .apply(lambda x: str(x) + '/' + str(yr))
    )

  #Validate data
  validate_data(df)
        
  # Filter Data
  data = (df
          .query( 'depart_city != "VCP" & ticket_prices > 0' )
          )

  # Load retrieved flight prices to the Postgres DB
  # Insert the data into the existing table
  data.to_sql("flight_prices", 
              engine, 
              if_exists="append", 
              index=False, 
              method="multi")

  st.write(f":floppy_disk: {df.shape[0]} Rows Loaded succesfully")
  return "Loaded"

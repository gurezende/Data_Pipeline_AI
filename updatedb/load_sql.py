# '''This script is to load the flights data to a Postgres Database.'''

# Imports
import pandas as pd
from updatedb.data_contract import validate_data
import streamlit as st
# Function to run DBT models
import subprocess
import os

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
  data.to_sql(name="flight_prices", 
              con=engine, 
              if_exists="append", 
              index=False, 
              method="multi")

  st.write(f":floppy_disk: {df.shape[0]} Rows Loaded succesfully")
  return "Loaded"




def run_dbt():
  """Runs dbt run from the flight_dbt directory."""

  try:
    # Path to your dbt project directory
    dbt_project_path = "./flights_dbt"
    # Execute the dbt run command
    subprocess.run(["dbt", "run"], cwd=dbt_project_path)
  except subprocess.CalledProcessError as e:
    print(f"Error running dbt: {e}")
    print(e.stderr)
  except FileNotFoundError:
    print("dbt executable not found. Make sure dbt is installed and in your PATH.")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

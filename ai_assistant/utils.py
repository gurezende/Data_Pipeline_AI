# Scrip to fetch and format data from DB Silver Layer

import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# Load environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME") 
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Database connection parameters
DB_CONFIG = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": 5432
}

def fetch_flight_data():
    query = """
    SELECT id, dt, depart_city, depart_time, city_arrival, time_arrival, 
           flight_numbers, stops, flight_lengths, ticket_prices, days_before_flight
    FROM silver_flights
    """
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql(query, conn)
    conn.close()
    print(f"Extracted {len(df)} flight records from the database!")
    return df


# Format data for vectorization
def format_flight_data(df):
    """Converts the DataFrame into a list of structured text documents for vectorization."""
    formatted_texts = []
    
    for _, row in tqdm(df.iterrows(), total=len(df)):
        text = (f"Flight from {row['depart_city']} to {row['city_arrival']} on {row['dt']}.\n"
                f"Departure: {row['depart_time']}, Arrival: {row['time_arrival']}.\n"
                f"Flight Number(s): {row['flight_numbers']}.\n"
                f"Stops: {row['stops']}.\n"
                f"Duration: {row['flight_lengths']}.\n"
                f"Price: {row['ticket_prices']} USD.\n"
                f"Booked {row['days_before_flight']} days before departure.")
        
        formatted_texts.append(text)

    print(f"Formatted {len(formatted_texts)} flight records for vectorization!")
    return formatted_texts


def search_flights(collection,query, top_k=3):
    """Retrieve relevant flights based on a natural language query."""
      
    # Search ChromaDB for similar embeddings
    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )
    
    return results['documents'][0] if results['documents'] else []


# test
if __name__ == "__main__":	
    # Run extraction
    flight_data = fetch_flight_data()
    print(flight_data.head())  # Check if data is extracted correctly

        # Format the data
    flight_texts = format_flight_data(flight_data)
    print(flight_texts[:2])  # Print first two entries to check the format


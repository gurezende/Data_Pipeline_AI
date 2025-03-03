# This script is to update the DB with new flight prices

# Imports
from webscraping import get_flights, get_date
from parser import *
from load_sql import load_to_sql
import streamlit as st
import pandas as pd


def update_db(d, origin_cd='ZFF', destin_cd='VCP'):    
    
    # Date to search
    search_date = get_date(add_days=d)
    st.write(f':page_with_curl: -- L O G --')
    st.write(f':calendar: Searching flights on {search_date}') 
    
    # Get Flights page
    get_flights(depart=origin_cd,
                arrivl=destin_cd,
                date_depart= search_date,
                days_range= 5)
    
    # Open HTML file
    soup = open_file('data/flights.html')

    # Find departures
    departures = soup.find_all("div", class_="flight-card__info left-container css-vjjku5")

    # Creating lists to store the values from the text
    dt = [] #flight date
    depart_city = [] #city departure
    depart_time = [] #departure times
    city_arrival = [] #city arrival
    time_arrival = [] #arrival times
    flight_numbers = [] #flight numbers
    n_stops = [] # qty of stops
    flight_lengths = [] # length in hours
    ticket_prices = [] #ticket prices

    st.write(':mag: Extracting data from HTML file...')

    for element in departures:
        # Extract departure data
        departure_city, departure_date, departure_time = departure_information(element=element)
        # Append to list
        depart_city.append(departure_city)
        dt.append(departure_date)
        depart_time.append(departure_time)
        
        # Extract arrival data
        arrival_city, arrival_time = arrival_information(element=element)
        # Append to list
        city_arrival.append(arrival_city)
        time_arrival.append(arrival_time)
        
        # Extract flight data
        flight_number, stops, hours_length = flight_information(element=element)
        # Append to list
        flight_numbers.append(flight_number)
        n_stops.append(stops)
        flight_lengths.append(hours_length)
        
        # Extract ticket Prices data
        ticket_prices = prices_information(soup)
        # IF ticket prices column is smaller than the number of dates, then add 0.
        while len(ticket_prices) < len(dt): ticket_prices.append('0')
    
    # First match of the search is usually a "same-day flight".
    # Make the date equal to the second entry
    dt[0] = dt[1]
    
    # Build DataFrame and fill missing values
    dtf_flights = pd.DataFrame({
        'dt': dt,
        'depart_city': depart_city,
        'depart_time': depart_time,
        'city_arrival': city_arrival,
        'time_arrival': time_arrival,
        'flight_numbers': flight_numbers,
        'n_stops': n_stops,
        'flight_lengths': flight_lengths,
        'ticket_prices': ticket_prices,
        'days_before_flight': [str(d)] * len(dt)
        }).ffill().bfill()
        
    
    #Save data as a table
    dtf_flights.to_csv('data/flights.csv', index=False)
    
    # Validate with Pandera and Load to SQL
    load_to_sql(flight_date= search_date)
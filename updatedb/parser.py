# This script is to parse the HTML file and extract flight information

# Imports 
from bs4 import BeautifulSoup
import numpy as np
import re


def open_file(file_path):
    '''Function to open the HTML file for parsing and convert to Beautiful Soup object
    * Input:
    path: file path to open
    '''
    f = open(file_path, 'r').read()
    # Convert html to a BeatufulSoup object
    bsoup = BeautifulSoup(f, 'html.parser')

    return bsoup

##################################################

def departure_information(element):
    '''
    Extract departure information from a BeautifulSoup element
    '''
    # Extract departure information
    departure_info = (element
                      .find('h4', class_=re.compile(r"^departure css-")))
    
    departure_city = (departure_info
                      .find('span', class_='iata-day')
                      .text
                      .strip()
                      .split(' • ')[0])
    departure_date = (departure_info
                      .find('span', class_='iata-day')
                      .text
                      .strip()
                      .split(' • '))
    # If no date is provided, use "-"
    if len(departure_date) == 1: 
        departure_date = np.nan
    else:
        departure_date = departure_date[1]
    
    # Parsing Departure Time
    departure_time = (departure_info
                      .text
                      .split()[0])

    

    return departure_city, departure_date, departure_time

##################################################

def arrival_information(element):
    '''
    Extract arrival information from a BeautifulSoup element.
    '''
    # Extract arrival information
    arrival_info = (element
                    .find('h4', class_=re.compile('arrival css-')))
    arrival_time = (arrival_info
                    .text
                    .strip()
                    .replace('\n', '')
                    .split(' ')[0])
    arrival_city = (arrival_info
                    .find('span', class_='iata-day')
                    .text
                    .strip()
                    .split(' • ')[0])

    return arrival_city, arrival_time

##################################################

def flight_information(element):
    '''Extract fligh number, qty of connections and duration of the flight from bs4 element'''
    
    # Extract stops and flight number
    leg_info = (element
                .find('span', class_='css-tkxfs6')
                .text
                .strip())

    flight_number = re.search('Voo [0-9]*', leg_info).group()
    stops = re.search('[0-9] conex|Direto', leg_info).group()

    # Extract flight length
    flight_length = (element
                     .find('button', class_=re.compile('duration css-'))
                     .find('strong')
                     .text
                     .strip()
                     .split())
    
    # Transform days into hours
    if 'd' in flight_length[0]:
        day_length = int(flight_length[0].split('d')[0])*24
        if len(flight_length) < 2:
            flight_length.extend(['0h', '0m']) # When the flight is 1d, add 0h and 0m
        elif len(flight_length) < 3:
            flight_length.extend(['0m']) # When the flight is 1d 8h, add 0m
        hr_length = int(flight_length[1].split('h')[0]) + day_length
        min_length = int(flight_length[2].split('m')[0])
    else:
        # Convert to integer
        hr_length = int(flight_length[0].split('h')[0])
        if len(flight_length) < 2: flight_length.append('0m') #if flight is 8h0m, the min is not displayed, so we need to add.
        min_length = int(flight_length[1].split('m')[0])
    
    # Convert to hours
    hours_length = hr_length + (min_length/60)
    
    return flight_number, stops, hours_length

##################################################

def prices_information(soup):
    '''Extract ticket prices of the flight from a bs4 element'''

    parsed_prices = []

    # Find prices
    # price_elements = soup.find_all('h4', class_='current css-2db79l')
    price_elements = soup.find_all('div', class_=re.compile('flight-card__fare right-container'))

    # Iterate and collect ticket prices
    for p in price_elements:
        price=(
            p
            .text
            .strip()
            .replace('R$', '')
            .replace('.', '')
            .replace('\n','')
            .replace('A partir de','')
            .replace('Voo esgotado','0-')
            .replace(' ','')
            .replace('0-0-','0')
            .split(',')[0]
            .strip()
        )

        # Price to float
        price = float(price)

        # Append to list
        parsed_prices.append(price)
    
    return parsed_prices


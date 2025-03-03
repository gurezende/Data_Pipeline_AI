'''
Script to open the airline website, browse the flights and get HTML file for parsing.
'''

# Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import datetime
import time
import streamlit as st


def get_date(add_days=0):
    '''
    Get current system date and put in format dd/mm/yyyy
    * add_days: int = how many days to add to the current date
    '''
    
    # Get system's time
    current_time = datetime.datetime.now() #get current system date
    
    # Add days if applicable
    new_date = (current_time + datetime.timedelta(days=add_days)).strftime('%d/%m/%Y')
    
    # convert to date format
    new_date = datetime.datetime.strptime(new_date, '%d/%m/%Y').strftime('%d/%m/%Y')

    return new_date #dd/mm/yyyy


def get_flights(depart, arrivl, date_depart='today', days_range=10):
    '''
    Open a browser, search for flights between the chosen cities and dates, and save resulting html page.
    
    - -Inputs- -
    * depart: str = Code of the departure city airport. e.g. "FLL"
    * arrivl: str = Code of the arrival city airport. e.g. "VCP"
    * date_depart: str = date of departure in the format dd/mm/yyyy. Default: "today".
    * days_range: int = search between today + n days. e.g. 10
    '''
    #--------- Set start and end date of the range ------------

    # Set the default date of departure for the current system's date
    if date_depart == 'today':
        date_depart = get_date()

    # Set Final Date for the date range
    final_date = (datetime.datetime.strptime(date_depart, '%d/%m/%Y') + datetime.timedelta(days=days_range)).strftime('%d/%m/%Y')
    
    #--------- Browse and webscraping with Selenium ------------

    # Configuring Browser Options
    chrome_options = Options()
    # chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-cookies")

    # Opening Driver to use the pointer in browser
    driver = webdriver.Chrome(options=chrome_options)
    driver.minimize_window()

    # Open Azul Airlines website
    driver.get("https://www.voeazul.com.br/br/pt/home")
    
    # Click on the Cookies accept button
    time.sleep(2)
    cookie_ok_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler")))
    cookie_ok_button.click()

    # Complete Origin Search Box
    origin = driver.find_element(By.CSS_SELECTOR, '#Origem1')
    origin.send_keys(depart)
    time.sleep(5)
    origin.send_keys(Keys.RETURN)

    # Complete Destination Search Box
    destin = driver.find_element(By.CSS_SELECTOR, "#Destino1")
    destin.send_keys(arrivl)
    time.sleep(1)
    destin.send_keys(Keys.RETURN)

    # Click on the Dates Search Button to open fields to input dates
    driver.find_element(By.CSS_SELECTOR, "#datepicker_temp1").send_keys(Keys.RETURN)

    # Wait page load
    time.sleep(1)

    ### Complete DATES RANGE
    print(date_depart)
    # Start Date
    start_date = driver.find_element(By.CSS_SELECTOR, "#startDate")
    start_date.send_keys(date_depart) #dd/mm/yyyy

    # End Date = Start + 10
    end_date = driver.find_element(By.ID, "endDate")
    end_date.send_keys(final_date) #dd/mm/yyyy

    # Click Button "Fechar"
    driver.find_element(By.CSS_SELECTOR, 'button[tabindex="0"]').click()

    # Click Button "Confirmar"
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="search-box-hotel-date-picker-primary-button"]').click()

    time.sleep(25)

    # Get page HTML
    html_doc = driver.page_source
    soup = BeautifulSoup(html_doc, 'html.parser').prettify()

    # Close Chrome driver
    driver.quit()

    #--------- Save HTML file to data folder ------------

    # Save file
    file = open('data/flights.html', 'w')
    file.write(soup)
    file.close()

    st.write(":airplane: Flights.html successfully saved!")

    return "Flights.html successfully saved!"

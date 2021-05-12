# Importing Beautifulsoup for webscrapping and Selenium for webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
# Importing request module to get the URL and time module to increase the screen time
import requests
import time

# Setting the chromedriver path
chrome_path = '/Users/Cassa/chromedriver'

# Setting your google form URL prehand
GOOGLE_FORM_URL = 'https://forms.gle/dGC3iEfEbhKMrv7FA'

# Setting the URL of the specific search depending upon your requirements
URL = 'https://www.99acres.com/search/property/buy/kharadi?city=19&bedroom_num=2&class=A&locality=839&preference=S&area_unit=1&budget_max=125&budget_min=120&availability=1%2C2&res_com=R'

response = requests.get(URL)

contents = response.text

# Initialising the soup for scrapping
soup = BeautifulSoup(contents, 'html.parser')

# To get all the property names
properties = soup.find_all(name='td', class_='list_header_bold')

property_names = []
for property_name in properties:
    try:
        property_names.append(property_name.a.text)
    except AttributeError:
        pass

# To get all the links linked to certain property
property_links = []
for property_link in properties:
    try:
        property_links.append(property_link.a.get('href'))
    except AttributeError:
        pass


# To get the prices of the properties
prices = soup.find_all(name='td', attrs={'id': 'srp_tuple_price'})
property_prices = [property_price.getText().split('₹')[1] for property_price in prices]

# Initialising the driver for automation
driver = webdriver.Chrome(executable_path=chrome_path)

# Get the form
driver.get(GOOGLE_FORM_URL)

# Loop to fill the form everytime with entries from prices, name, and links
for i in range(len(property_names)):
    # Filling the name of the property
    name = driver.find_element_by_css_selector('[aria-labelledby="i1"]')
    time.sleep(1)
    name.send_keys(f'{property_names[i]}')

    # Filling the price of the property
    price = driver.find_element_by_css_selector('[aria-labelledby="i5"]')
    time.sleep(1)
    price.send_keys(f'{property_prices[i]}')

    # Filling the link of the property
    link = driver.find_element_by_css_selector('[aria-labelledby="i9"]')
    time.sleep(1)
    link.send_keys(f'https://www.99acres.com{property_links[i]}')

    # Submitting the form with previous entries
    submit = driver.find_element_by_css_selector('[role="button"]')
    time.sleep(1)
    submit.click()

    # Submit another response
    submit_another_form = driver.find_element_by_link_text('Submit another response')
    submit_another_form.click()
    time.sleep(1)

## Make sure while creating the google form the sequence is exactly like this or else make the necessary changes

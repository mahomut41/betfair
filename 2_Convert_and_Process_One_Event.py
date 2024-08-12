#Open historical data (API) page and using my username and password to login 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os
from selenium.webdriver.common.keys import Keys


# Configuration of the Chrome webdriver
options = webdriver.ChromeOptions()

# Initialize the Chrome webdriver
driver = webdriver.Chrome(options=options)
# setup notebook 
import pandas as pd
pd.plotting.register_matplotlib_converters()
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
print("Setup Complete")

import numpy as np
import pandas as pd

### Go to historic data processor page


driver.get('https://www.betfairhistoricdata.co.uk/')

# Find the file input element
file_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
)
### select file from /Downloads 
### file is in the selected path, (the biggest file was selected to see all market types)
# Specify the path to the file you want to upload
file_path = "/Users/noahroni/Documents/event_files/33024145.bz2"

# Upload the file
file_input.send_keys(file_path)

time.sleep(15)

# Find all market type elements
market_type_elements = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-virtual-scroll']//div[@class='v-list-item__title']"))
)

# Find the button by CSS selector based on the span text
download_settings_button = driver.find_element(By.CSS_SELECTOR, "button.v-btn--fab.v-btn--plain.v-btn--round.theme--light.v-size--small span.v-btn__content")

# Click on the button two times
download_settings_button.click()

time.sleep(1)




try:
    # Wait for the icon element to be clickable
    icon_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light']"))
    )

    # Click on the icon element
    icon_element.click()
except Exception as e:
    try:
        # Find the input element by its ID using WebDriverWait
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "input-73"))
        )
        
        # Click on the input element
        input_element.click()
        
    except Exception as e:
        print(f"Error occurred while clicking the input element: {e}")
       


options_to_select = [
    "md.eventName",
    "md.name",
    "numberOfActiveRunners",
    "numberOfWinners",
    "status",
    "totalMatched"
]

# Find the input element
input_element = driver.find_element(By.XPATH, "//input[@id='input-61']")

# Iterate through the options to select
for option in options_to_select:
    # Clear the input field
    input_element.clear()
    
    # Type the option into the input field
    input_element.send_keys(option)
    
    # Press the "Enter" key to select the option
    input_element.send_keys(Keys.ENTER)
    
time.sleep(2) 
try:
    # Wait for the element to be clickable
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@class='v-card__title']/span[@class='text-h5']"))
    )

    # Click on the element
    element.click()
except Exception as e:
    print(f"Error occurred while clicking on the element: {e}")


time.sleep(2)

try:
    # Find the label element
    label_element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//label[@for='input-83' and contains(text(), 'Selection Columns')]"))
    )
    
    # Click on the label element
    label_element.click()
except Exception as e:
    print(f"Error occurred while clicking on the label: {e}")

# Find the label element by its "for" attribute value
label_element = driver.find_element(By.CSS_SELECTOR, 'label[for="input-71"]')

# Click on the label element
label_element.click()


options_to_select = [
    "md.name",
    "ex.availableToBack.price",
    "ex.availableToBack.size",
    "ex.availableToLay.price",
    "ex.availableToLay.size",
    "status",
    "totalMatched"
]

# Find the input element
input_element = driver.find_element(By.XPATH, "//input[@id='input-71']")

# Iterate through the options to select
for option in options_to_select:
    # Clear the input field
    input_element.clear()
    
    # Type the option into the input field
    input_element.send_keys(option)
    
    # Press the "Enter" key to select the option
    input_element.send_keys(Keys.ENTER)
    

try:
    # Find the element by XPath
    close_icon_element = driver.find_element(By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light secondary--text']")

    # Click on the close icon element
    close_icon_element.click()
except Exception as e:
    print(f"Error occurred while clicking on the close icon: {e}")
try:
    # Find the element by XPath
    close_icon_element = driver.find_element(By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light secondary--text']")

    # Click on the close icon element
    close_icon_element.click()
except Exception as e:
    print(f"Error occurred while clicking on the close icon: {e}")

### if we want to desactive preplay output option !!!
time.sleep(2)
# Assuming you have initialized your WebDriver instance as 'driver'

# Find the div element by its class name
div_element = driver.find_element(By.CLASS_NAME, 'v-input--selection-controls__ripple')

# Click on the div element
div_element.click()


# Find the input element by its ID
input_element = driver.find_element(By.ID, 'input-89')

# Click on the input element
input_element.click()
time.sleep(1)
### we can select time frequency 
### for this we selected 60s. to change time, modify this --> '//div[@id="list-89"]//div[text()=" 60s "]'. Write 0.5s, 1s, 2s, 5s, 10s, 60s or 600s .
# Find the div element by its text content
div_element = driver.find_element(By.XPATH, '//div[text()=" 60s "]')

# Click on the div element
div_element.click()


try:
    # Find the Save button
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "save")]'))
    )
    
    # Click on the Save button
    save_button.click()
except Exception as e:
    print(f"Error occurred while clicking on the Save button: {e}")
time.sleep(1)

try:
    # Find the Download CSV button
    download_csv_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download csv")]'))
    )
    
    # Click on the Download CSV button
    download_csv_button.click()
except Exception as e:
    print(f"Error occurred while clicking on the Download CSV button: {e}")

time.sleep(15)

### to convert from zip to csv format

# Find the main content element
main_content_element = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//div[@class="v-card__text"]'))
)

# Extract the text from the main content element
main_content_text = main_content_element.text

# Use regular expression to find Market ID
market_id_match = re.search(r'Market Id: (\d+\.\d+)', main_content_text)
if market_id_match:
    market_id = market_id_match.group(1)
    # Print the Market ID
    print(f"Market Id: {market_id}")
else:
    print("Market ID not found in the main content text.")


def open_file_in_folder(file_path):
    try:
        # Open the file by executing a command-line operation
        os.system(f'open "{file_path}"')  # For Mac
    except Exception as e:
        print(f"Error occurred while opening the file: {e}")

# Define the path to the Downloads folder
home_dir = os.path.expanduser("~")
download_folder = os.path.join(home_dir, 'Downloads')

# Define the path to the downloaded zip file (assuming it's already downloaded)
market_id_zip_file = os.path.join(download_folder, f"{market_id}.zip")

# Call the function to open the downloaded zip file
open_file_in_folder(market_id_zip_file)

# Define the path to the downloaded zip file (assuming it's already downloaded)
market_id_csv_file = os.path.join(download_folder, f"{market_id}.csv")

print(market_id_csv_file)

time.sleep(1)

# Read the file
market_id_data = pd.read_csv(market_id_csv_file ) #could be added " index_col="publishTime", parse_dates=True"

market_id_data.tail()

# Define a function to apply the formula and rounding to each row
def calculate_and_round_percentage(row):
    if row['totalMatched'] == 0 or row['selection_totalMatched'] == 0:
        return 0
    else:
        percentage = (row['selection_totalMatched'] / row['totalMatched']) * 100
        return round(percentage, 2)

# Add a new column with the calculated and rounded percentage
market_id_data['percent_money_on_market'] = market_id_data.apply(calculate_and_round_percentage, axis=1)

# Display the DataFrame with the new column
market_id_data.tail()

# Convert specific columns to float data type, handling non-numeric values
columns_to_convert = ['totalMatched', 'selection_ex.availableToBack.price', 'selection_ex.availableToBack.size',
                      'selection_ex.availableToLay.price', 'selection_ex.availableToLay.size', 'selection_totalMatched']

for col in columns_to_convert:
    market_id_data[col] = pd.to_numeric(market_id_data[col], errors='coerce')

# Display the DataFrame with the new column
market_id_data.head()
# Format 'publishTime' column as 'YYYY-MM-DD HH:MM:SS.%f'
market_id_data['publishTime'] = market_id_data['publishTime'].apply(lambda x: pd.to_datetime(x).strftime('%Y-%m-%d %H:%M:%S.%f'))

# Convert 'publishTime' column to datetime format
market_id_data['publishTime'] = pd.to_datetime(market_id_data['publishTime'], format='%Y-%m-%d %H:%M:%S.%f')

# Get the first publishTime as the start time
start_time = market_id_data['publishTime'].iloc[0]

# Calculate the minute difference from the start time for each publishTime
market_id_data['Minute'] = ((market_id_data['publishTime'] - start_time).dt.total_seconds() / 60 + 1).astype(int)

# Format the 'publishTime' column as 'DD.MM.YYYY HH:MM:SS'
market_id_data['publishTime'] = market_id_data['publishTime'].dt.strftime('%d.%m.%Y %H:%M:%S')    

time.sleep(1)


# Check if 90 minutes have passed and if the percent of money is 0
market_id_data['Status'] = ''
for index, row in market_id_data.iterrows():
    if row['Minute'] > 90 and row['percent_money_on_market'] == 0:
        market_id_data.at[index, 'Status'] = 'Match ended'

# Construct the custom filename
event_name = market_id_data['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_')
market_name = market_id_data['md.name'].iloc[0].replace(' ', '').replace('/', '_')
filename = f'{event_name}({market_name}).csv'

# Create a folder with the event name if it doesn't exist
folder_path = event_name
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Define the full file path
file_path = os.path.join(folder_path, filename)

# Write the DataFrame to a CSV file with the custom filename
market_id_data.to_csv(file_path, index=False, float_format='%.2f', na_rep='NaN')

# Display the DataFrame with the new column
market_id_data.tail()

# Define a list of file paths to remove
files_to_remove = [
    os.path.join(download_folder, f"{market_id}.zip"),
    os.path.join(download_folder, f"{market_id}.csv")
]

# Iterate over each file path in the list
for file_path in files_to_remove:
    # Check if the file exists
    if os.path.exists(file_path):
        # If it exists, remove it
        os.remove(file_path)

# Quit the WebDriver instance and close the browser
driver.quit()

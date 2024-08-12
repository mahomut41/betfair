# Standard Library Imports
import os
import re
import time
import subprocess
import zipfile

# Third-Party Imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException, 
    ElementNotInteractableException, 
    NoSuchElementException
)

# Matplotlib Converter Registration
pd.plotting.register_matplotlib_converters()

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False  # Keep the browser window open

# Configuration of the Chrome webdriver
options = webdriver.ChromeOptions()

# Create a WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

# Specify the path to the directory containing the files
directory_path = "/Users/noahroni/Documents/Market_Folders_bz2"

# Create the error folder path
error_folder_path = "/Users/noahroni/Documents/Market_Folders_csv_error"

if not os.path.exists(error_folder_path):
    os.makedirs(error_folder_path)

# Iterate over all files in the directory
for file_name in os.listdir(directory_path):

    if file_name == ".DS_Store":
        continue  # Skip the .DS_Store file

    file_paths = os.path.join(directory_path, file_name)

    try:
        driver.get('https://www.betfairhistoricdata.co.uk/')
       

        # Find the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        # Upload the file
        file_input.send_keys(file_paths)
        time.sleep(1)
       
        # Find all market type elements
        market_type_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-virtual-scroll']//div[@class='v-list-item__title']"))
        )
        # Scroll down to ensure the button is in view
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for scrolling to complete
        download_settings_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn--fab.v-btn--plain.v-btn--round.theme--light.v-size--small span.v-btn__content"))
        )
        # Click on the button two times
        download_settings_button.click()
       

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

        # Wait until the input element is present
        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='input-60']"))
            )
        except Exception as e:
            try:
                    # Fallback: Click on the div element
                input_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='v-input__append-inner']/div[@class='v-input__icon v-input__icon--append']"))
                )
            except Exception as e:
                try:
                    # Wait for the element to be clickable
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='v-card__title']/span[@class='text-h5']"))
                    )

                    # Click on the element
                    element.click()
                except Exception as e:
                    print(f"Error occurred while clicking on the element: {e}")
        
        # Iterate through the options to select
        for option in options_to_select:

            # Clear the input field if it is interactable
            attempts = 0
            while attempts < 2:
                try:
                    input_element.clear()
                    break
                except ElementNotInteractableException:
                    #time.sleep(0.02)
                    attempts += 1
            
            # Type the option into the input field
            input_element.send_keys(option)
            
            # Press the "Enter" key to select the option
            input_element.send_keys(Keys.ENTER)

        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='v-card__title']/span[@class='text-h5']"))
            )

            # Click on the element
            element.click()
        except Exception as e:
            print(f"Error occurred while clicking on the element: {e}")

        # Find the label element by its "for" attribute value
        label_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="input-70"]'))
        )

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
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='input-70']"))
        )

        # Iterate through the options to select
        for option in options_to_select:

            # Wait for the input element to be clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(input_element)
            )

            # Clear the input field if it is interactable
            attempts = 0
            while attempts < 2:
                try:
                    input_element.clear()
                    break
                except ElementNotInteractableException:
                    #time.sleep(1)
                    attempts += 1

            # Type the option into the input field
            input_element.send_keys(option)
            
            # Press the "Enter" key to select the option
            input_element.send_keys(Keys.ENTER)  

        try:
            # Find the element by XPath
            close_icon_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light secondary--text']"))
            )

            # Click on the close icon element
            close_icon_element.click()
        except Exception as e:
            print(f"Error occurred while clicking on the close icon: {e}")

        # Find the div element by its class name
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'v-input--selection-controls__ripple'))
        )

        # Click on the div element
        div_element.click()

        # Find the input element by its ID
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'input-88'))
        )

        # Click on the input element
        input_element.click()

        # Find the div element by its text content
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()=" 60s "]'))
        )

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

        max_counts = 24
        click_count = 0

        # Keep track of clicked elements
        clicked_elements = set()

        # Continue looping until we reach the maximum number of scrolls
        while click_count < max_counts:
            # Find all market type elements
            market_type_elements = driver.find_elements(By.CLASS_NAME, "v-list-item__title")
            
            # Track if any new element was clicked in this iteration
            new_element_clicked = False

            # Iterate over each market type element
            for market_type_element in market_type_elements:
                # Check if the element has already been clicked
                if market_type_element.text not in clicked_elements:

                    max_attempts = 5  # Maximum number of attempts to make the element clickable
                    attempt = 0

                    while attempt < max_attempts:
                        # Scroll the market type element halfway into view using JavaScript
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)

                        try:
                            # Wait for the element to be clickable
                            wait = WebDriverWait(driver, 10)
                            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "v-list-item__title")))
                            #time.sleep(0.1)
                            
                            # Click the element
                            market_type_element.click()

                            # Break the loop if the click was successful
                            break
                        except:
                            # Increment the attempt counter
                            attempt += 1
                        #time.sleep(1)

                    # Add the element to the set of clicked elements
                    clicked_elements.add(market_type_element.text)
                    
                    # Increment the scroll count
                    click_count += 1

                    # Indicate that a new element was clicked
                    new_element_clicked = True
                    
                    # Scroll the market type element halfway into view using JavaScript
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)
                    #time.sleep(1)
                    try:
                            # Find the Download CSV button
                        download_csv_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download csv")]'))
                        )
                            
                            # Click on the Download CSV button
                        download_csv_button.click()
                        time.sleep(15)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)


                    except Exception as e:
                            # Scroll down to ensure the button is in view
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #time.sleep(1)  # Wait for scrolling to complete
                            
                            # Find the Download CSV button
                        download_csv_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download csv")]'))
                        )
                            
                            # Click on the Download CSV button
                        download_csv_button.click()
                        time.sleep(15)
                        
                        # Scroll back up to the top of the page
                        driver.execute_script("window.scrollTo(0, 0);")        
                        # Execute JavaScript to set the viewport height to the height of the entire page
                        #time.sleep(1)  # Wait for scrolling to complete       

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
                    else:
                        print("Market ID not found in the main content text.")

                    #def open_file_in_folder(file_path):
                     #   try:
                            # Open the file by executing a command-line operation
                      #      os.system(f'open "{file_path}"')  # For Mac
                       # except Exception as e:
                        #    print(f"Error occurred while opening the file: {e}")

                    # Define the path to the Downloads folder
                    home_dir = os.path.expanduser("~")
                    download_folder = os.path.join(home_dir, 'Downloads')

                    # Define a flag to track if the action has been performed
                    action_performed = False
                    # Check if the ZIP file exists and if the action hasn't been performed yet
                    if f"{market_id}.zip" in os.listdir(download_folder) and not action_performed:
                        # Set the flag to True to indicate that the action has been performed
                        action_performed = True
                        
                        # Define the path to the downloaded zip file (assuming it's already downloaded)
                        market_id_zip_file = os.path.join(download_folder, f"{market_id}.zip")

                        # Call the function to open the downloaded zip file
                        #open_file_in_folder(market_id_zip_file)

                        f = zipfile.ZipFile(market_id_zip_file)
                        f.extract(f.infolist()[0], download_folder)

                    
                      

                        # Define the path to the downloaded zip file (assuming it's already downloaded)
                        market_id_csv_file = os.path.join(download_folder, f"{market_id}.csv")

                       

                        # Read the file
                        market_id_data = pd.read_csv(market_id_csv_file ) #could be added " index_col="publishTime", parse_dates=True"

                        # Define a function to apply the formula and rounding to each row
                        def calculate_and_round_percentage(row):
                            if row['totalMatched'] == 0 or row['selection_totalMatched'] == 0:
                                return 0
                            else:
                                percentage = (row['selection_totalMatched'] / row['totalMatched']) * 100
                                return round(percentage, 2)

                        # Add a new column with the calculated and rounded percentage
                        market_id_data['percent_money_on_market'] = market_id_data.apply(calculate_and_round_percentage, axis=1)

                        # Convert specific columns to float data type, handling non-numeric values
                        columns_to_convert = ['totalMatched', 'selection_ex.availableToBack.price', 'selection_ex.availableToBack.size',
                                            'selection_ex.availableToLay.price', 'selection_ex.availableToLay.size', 'selection_totalMatched']

                        for col in columns_to_convert:
                            market_id_data[col] = pd.to_numeric(market_id_data[col], errors='coerce')
                         

                        # Format 'publishTime' column as 'YYYY-MM-DD HH:MM:SS.%f'
                        market_id_data['publishTime'] = market_id_data['publishTime'].apply(lambda x: pd.to_datetime(x).strftime('%d.%m.%Y %H:%M:%S.%f'))

                        # Convert 'publishTime' column to datetime format
                        market_id_data['publishTime'] = pd.to_datetime(market_id_data['publishTime'], format='%d.%m.%Y %H:%M:%S.%f')

                        # Get the first publishTime as the start time
                        start_time = market_id_data['publishTime'].iloc[0]

                        # Calculate the minute difference from the start time for each publishTime
                        market_id_data['Minute'] = ((market_id_data['publishTime'] - start_time).dt.total_seconds() / 60 + 1).astype(int)

                        # Format the 'publishTime' column as 'DD.MM.YYYY HH:MM:SS'
                        market_id_data['publishTime'] = market_id_data['publishTime'].dt.strftime('%d.%m.%Y %H:%M:%S')    

                        # Check if 90 minutes have passed and if the percent of money is 0
                        market_id_data['Status'] = ''
                        for index, row in market_id_data.iterrows():
                            if row['Minute'] > 90 and row['percent_money_on_market'] == 0 and row['status'] == "CLOSED":
                                market_id_data.at[index, 'Status'] = 'Match ended'

                        # Construct the custom filename
                        event_name = market_id_data['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                        market_name = market_id_data['md.name'].iloc[0].replace(' ', '').replace('/', '')
                        filename = f'{event_name}({market_name}).csv' # dont forget to erase ""

                        # Define the main folder and event name
                        main_folder = "/Users/noahroni/Documents/Betfair/Market_Folders_csv(final)"
                        # Create the main folder if it doesn't exist
                        if not os.path.exists(main_folder):
                            os.makedirs(main_folder)

                        # Define the full path for the event folder
                        folder_path = os.path.join(main_folder, event_name)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)

                        # Define the full file path
                        file_path = os.path.join(folder_path, filename)

                        # Write the DataFrame to a CSV file with the custom filename
                        market_id_data.to_csv(file_path, index=False, float_format='%.2f', na_rep='NaN')

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
                        

            # If no new element was clicked in this iteration, break the loop
            if not new_element_clicked:
                break
            
        # Remove the file after processing
        os.remove(file_paths)

    except Exception as e:
        print(f"Error occurred while processing file '{file_paths}': {e}")
        # Move the file to the error folder
        error_file_path = os.path.join(error_folder_path, file_name)
        os.rename(file_paths, error_file_path)
        print(f"Moved file '{file_paths}' to the error folder '{error_folder_path}'.")

# Quit the driver
driver.quit()

# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.headless = False  # Keep the browser window open

# Configuration of the Chrome webdriver
options = webdriver.ChromeOptions()

# Create a WebDriver instance
driver = webdriver.Chrome(options=chrome_options)

# Specify the path to the directory containing the files
directory_path = "/Users/noahroni/Documents/Market_Folders_bz2"

# Create the error folder path
error_folder_path = "/Users/noahroni/Documents/Market_Folders_csv(final)"

if not os.path.exists(error_folder_path):
    os.makedirs(error_folder_path)

# Iterate over all files in the directory
for file_name in os.listdir(directory_path):

    if file_name == ".DS_Store":
        continue  # Skip the .DS_Store file

    file_paths = os.path.join(directory_path, file_name)

    try:
        driver.get('https://www.betfairhistoricdata.co.uk/')
        time.sleep(1)

        # Find the file input element
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )

        # Upload the file
        file_input.send_keys(file_paths)
        time.sleep(3)
        
        # Find all market type elements
        market_type_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@class='v-virtual-scroll']//div[@class='v-list-item__title']"))
        )
        # Scroll down to ensure the button is in view
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for scrolling to complete
        download_settings_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.v-btn--fab.v-btn--plain.v-btn--round.theme--light.v-size--small span.v-btn__content"))
        )
        # Click on the button two times
        download_settings_button.click()
        time.sleep(0.3)

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

        # Wait until the input element is present
        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@id='input-61']"))
            )
        except Exception as e:
            try:
                    # Fallback: Click on the div element
                input_element = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[@class='v-input__append-inner']/div[@class='v-input__icon v-input__icon--append']"))
                )
            except Exception as e:
                try:
                    # Wait for the element to be clickable
                    element = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//div[@class='v-card__title']/span[@class='text-h5']"))
                    )

                    # Click on the element
                    element.click()
                except Exception as e:
                    print(f"Error occurred while clicking on the element: {e}")
        time.sleep(0.5)
        # Iterate through the options to select
        for option in options_to_select:

            # Clear the input field if it is interactable
            attempts = 0
            while attempts < 2:
                try:
                    input_element.clear()
                    break
                except ElementNotInteractableException:
                    #time.sleep(0.02)
                    attempts += 1
            
            # Type the option into the input field
            input_element.send_keys(option)
            
            # Press the "Enter" key to select the option
            input_element.send_keys(Keys.ENTER)

        try:
            # Wait for the element to be clickable
            element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@class='v-card__title']/span[@class='text-h5']"))
            )

            # Click on the element
            element.click()
        except Exception as e:
            print(f"Error occurred while clicking on the element: {e}")

        # Find the label element by its "for" attribute value
        label_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'label[for="input-71"]'))
        )

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
        input_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='input-71']"))
        )

        # Iterate through the options to select
        for option in options_to_select:

            # Wait for the input element to be clickable
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(input_element)
            )

            # Clear the input field if it is interactable
            attempts = 0
            while attempts < 2:
                try:
                    input_element.clear()
                    break
                except ElementNotInteractableException:
                    #time.sleep(1)
                    attempts += 1

            # Type the option into the input field
            input_element.send_keys(option)
            
            # Press the "Enter" key to select the option
            input_element.send_keys(Keys.ENTER)  

        try:
            # Find the element by XPath
            close_icon_element = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//i[@class='v-icon notranslate mdi mdi-menu-down theme--light secondary--text']"))
            )

            # Click on the close icon element
            close_icon_element.click()
        except Exception as e:
            print(f"Error occurred while clicking on the close icon: {e}")

        # Find the div element by its class name
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'v-input--selection-controls__ripple'))
        )

        # Click on the div element
        div_element.click()

        # Find the input element by its ID
        input_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'input-89'))
        )

        # Click on the input element
        input_element.click()

        # Find the div element by its text content
        div_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()=" 60s "]'))
        )

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

        max_counts = 24
        click_count = 0

        # Keep track of clicked elements
        clicked_elements = set()

        # Continue looping until we reach the maximum number of scrolls
        while click_count < max_counts:
            # Find all market type elements
            market_type_elements = driver.find_elements(By.CLASS_NAME, "v-list-item__title")
            
            # Track if any new element was clicked in this iteration
            new_element_clicked = False

            # Iterate over each market type element
            for market_type_element in market_type_elements:
                # Check if the element has already been clicked
                if market_type_element.text not in clicked_elements:

                    max_attempts = 5  # Maximum number of attempts to make the element clickable
                    attempt = 0

                    while attempt < max_attempts:
                        # Scroll the market type element halfway into view using JavaScript
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)

                        try:
                            # Wait for the element to be clickable
                            wait = WebDriverWait(driver, 10)
                            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "v-list-item__title")))
                            #time.sleep(0.1)
                            
                            # Click the element
                            market_type_element.click()

                            # Break the loop if the click was successful
                            break
                        except:
                            # Increment the attempt counter
                            attempt += 1
                        #time.sleep(1)

                    # Add the element to the set of clicked elements
                    clicked_elements.add(market_type_element.text)
                    
                    # Increment the scroll count
                    click_count += 1

                    # Indicate that a new element was clicked
                    new_element_clicked = True
                    
                    # Scroll the market type element halfway into view using JavaScript
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)
                    #time.sleep(1)
                    try:
                            # Find the Download CSV button
                        download_csv_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download csv")]'))
                        )
                            
                            # Click on the Download CSV button
                        download_csv_button.click()
                        time.sleep(15)
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", market_type_element)


                    except Exception as e:
                            # Scroll down to ensure the button is in view
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        #time.sleep(1)  # Wait for scrolling to complete
                            
                            # Find the Download CSV button
                        download_csv_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "Download csv")]'))
                        )
                            
                            # Click on the Download CSV button
                        download_csv_button.click()
                        time.sleep(15)
                        
                        # Scroll back up to the top of the page
                        driver.execute_script("window.scrollTo(0, 0);")        
                        # Execute JavaScript to set the viewport height to the height of the entire page
                        #time.sleep(1)  # Wait for scrolling to complete       

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
                    else:
                        print("Market ID not found in the main content text.")

                    #def open_file_in_folder(file_path):
                     #   try:
                            # Open the file by executing a command-line operation
                      #      os.system(f'open "{file_path}"')  # For Mac
                       # except Exception as e:
                        #    print(f"Error occurred while opening the file: {e}")

                    # Define the path to the Downloads folder
                    home_dir = os.path.expanduser("~")
                    download_folder = os.path.join(home_dir, 'Downloads')

                    # Define a flag to track if the action has been performed
                    action_performed = False
                    # Check if the ZIP file exists and if the action hasn't been performed yet
                    if f"{market_id}.zip" in os.listdir(download_folder) and not action_performed:
                        # Set the flag to True to indicate that the action has been performed
                        action_performed = True
                        
                        # Define the path to the downloaded zip file (assuming it's already downloaded)
                        market_id_zip_file = os.path.join(download_folder, f"{market_id}.zip")

                        # Call the function to open the downloaded zip file
                        #open_file_in_folder(market_id_zip_file)

                        f = zipfile.ZipFile(market_id_zip_file)
                        f.extract(f.infolist()[0], download_folder)

                    
                        time.sleep(0.1)

                        # Define the path to the downloaded zip file (assuming it's already downloaded)
                        market_id_csv_file = os.path.join(download_folder, f"{market_id}.csv")

                        time.sleep(1)

                        # Read the file
                        market_id_data = pd.read_csv(market_id_csv_file ) #could be added " index_col="publishTime", parse_dates=True"

                        # Define a function to apply the formula and rounding to each row
                        def calculate_and_round_percentage(row):
                            if row['totalMatched'] == 0 or row['selection_totalMatched'] == 0:
                                return 0
                            else:
                                percentage = (row['selection_totalMatched'] / row['totalMatched']) * 100
                                return round(percentage, 2)

                        # Add a new column with the calculated and rounded percentage
                        market_id_data['percent_money_on_market'] = market_id_data.apply(calculate_and_round_percentage, axis=1)

                        # Convert specific columns to float data type, handling non-numeric values
                        columns_to_convert = ['totalMatched', 'selection_ex.availableToBack.price', 'selection_ex.availableToBack.size',
                                            'selection_ex.availableToLay.price', 'selection_ex.availableToLay.size', 'selection_totalMatched']

                        for col in columns_to_convert:
                            market_id_data[col] = pd.to_numeric(market_id_data[col], errors='coerce')
                            time.sleep(0.5)

                        # Format 'publishTime' column as 'YYYY-MM-DD HH:MM:SS.%f'
                        market_id_data['publishTime'] = market_id_data['publishTime'].apply(lambda x: pd.to_datetime(x).strftime('%d.%m.%Y %H:%M:%S.%f'))

                        # Convert 'publishTime' column to datetime format
                        market_id_data['publishTime'] = pd.to_datetime(market_id_data['publishTime'], format='%d.%m.%Y %H:%M:%S.%f')

                        # Get the first publishTime as the start time
                        start_time = market_id_data['publishTime'].iloc[0]

                        # Calculate the minute difference from the start time for each publishTime
                        market_id_data['Minute'] = ((market_id_data['publishTime'] - start_time).dt.total_seconds() / 60 + 1).astype(int)

                        # Format the 'publishTime' column as 'DD.MM.YYYY HH:MM:SS'
                        market_id_data['publishTime'] = market_id_data['publishTime'].dt.strftime('%d.%m.%Y %H:%M:%S')    

                        # Check if 90 minutes have passed and if the percent of money is 0
                        market_id_data['Status'] = ''
                        for index, row in market_id_data.iterrows():
                            if row['Minute'] > 90 and row['percent_money_on_market'] == 0 and row['status'] == "CLOSED":
                                market_id_data.at[index, 'Status'] = 'Match ended'

                        # Construct the custom filename
                        event_name = market_id_data['md.eventName'].iloc[0].replace(' v ', '_').replace('/', '_').replace(' ', '')
                        market_name = market_id_data['md.name'].iloc[0].replace(' ', '').replace('/', '')
                        filename = f'{event_name}({market_name}).csv' # dont forget to erase ""

                        # Define the main folder and event name
                        main_folder = "/Users/noahroni/Documents/Betfair/Market_Folders_csv(all)"
                        # Create the main folder if it doesn't exist
                        if not os.path.exists(main_folder):
                            os.makedirs(main_folder)

                        # Define the full path for the event folder
                        folder_path = os.path.join(main_folder, event_name)
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)

                        # Define the full file path
                        file_path = os.path.join(folder_path, filename)

                        # Write the DataFrame to a CSV file with the custom filename
                        market_id_data.to_csv(file_path, index=False, float_format='%.2f', na_rep='NaN')

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
                        time.sleep(1)

            # If no new element was clicked in this iteration, break the loop
            if not new_element_clicked:
                break
            
        # Remove the file after processing
        os.remove(file_paths)

    except Exception as e:
        print(f"Error occurred while processing file '{file_paths}': {e}")
        # Move the file to the error folder
        error_file_path = os.path.join(error_folder_path, file_name)
        os.rename(file_paths, error_file_path)
        print(f"Moved file '{file_paths}' to the error folder '{error_folder_path}'.")

# Quit the driver
driver.quit()

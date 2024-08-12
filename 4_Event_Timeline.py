from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import base64

# Configuration of the Chrome webdriver
options = webdriver.ChromeOptions()

# Initialize the Chrome webdriver
driver = webdriver.Chrome(options=options)

driver.get('https://bfcharts.co.uk/#welcome')
time.sleep(1)
# Find the link by its class name
link = driver.find_elements(By.CLASS_NAME, 'title')

# Click on the link if it exists
if link:
    link[0].click()

time.sleep(3)

try:
    # Find the button by its ID and click on it
    button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    if button:
        button.click()
except:
    pass

# Find the username input field and enter the username
username_input = driver.find_element(By.XPATH, '//input[@placeholder="Email or Username"]')
username_input.send_keys('allisonrmartin')
time.sleep(3)

# Find the password input field and enter the password
password_input = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_input.send_keys('313577Pl,.')

time.sleep(3)

try:
    # Find the button by its ID and click on it
    button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    if button:
        button.click()
except:
    pass

# Find the login button by its class name and click on it
login_button = driver.find_element(By.CLASS_NAME, 'loginButton')
login_button.click()

time.sleep(3)

driver.get('https://bfcharts.co.uk/#welcome')
time.sleep(3)

# Find the link by its class name
link = driver.find_elements(By.CLASS_NAME, 'title')

# Click on the link if it exists
if link:
    link[0].click()

time.sleep(5)
# Find the menu by its id and click on it
menu_button = driver.find_element(By.ID, 'menu')
menu_button.click()

time.sleep(1)

# Find the "Demo data" element by its class name and click on it
demo_data_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Demo data')]")
demo_data_element.click()

time.sleep(1)

# Find the "Soccer" element by its text content and click on it
soccer_element = driver.find_element(By.XPATH, "//li[contains(text(), '⚽ Soccer')]")
soccer_element.click()

time.sleep(1)

# Find the "26 Apr 2022 Man City v Real Madrid" element by its text content and click on it
match_element = driver.find_element(By.XPATH, "//li[contains(text(), '📅 19 Nov 2019 San Marino v Russia')]")
match_element.click()

time.sleep(1)
# Define the CSS selector for the market element
market_selector = 'div.column li.market'

# Wait for the market element to be clickable
market_element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, market_selector))
)

# Click on the market element
market_element.click()

# Find the parent element with the ID "marketParent"
event_name = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "marketParent"))
)
event_name = event_name.text

# Print the text of the clicked parent element
print(event_name)
# Create a folder to save the screenshots
folder_name = 'Event_timeline'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Find the element containing the time section
time_element = driver.find_element(By.ID, 'subTitle')

time.sleep(2)

screenshot_path = f'{folder_name}/timeline_{event_name}.png'
# Capture a screenshot of the time section
time_element.screenshot(screenshot_path)


time.sleep(4)
# Create and write the print information to a text file
with open(f'{folder_name}/info_{event_name}.txt', 'w') as file:
    # Write the event name
    file.write(f'Event Name: {event_name}\n\n')
    
    # Write the print information
    file.write('Print Information:\n')
    
    # Find all event icons
    event_icons = driver.find_elements(By.CSS_SELECTOR, 'div.soccer.timeline .event')

    # Define the initial total duration of the match (in minutes)
    total_duration_minutes = 90  # Assuming a standard 90-minute match

    # Define the starting minute of the second half
    starting_minute_second_half = 45

    # Initialize a variable to keep track of the current minute
    current_minute = 0

    # Initialize a variable to keep track of any additional time
    additional_time = 0

    # Iterate through each event icon
    for event_icon in event_icons:
        # Get the style attribute
        style_attribute = event_icon.get_attribute('style')
        # Extract the position percentage from the style attribute
        position_percentage = float(style_attribute.split('left:')[1].split('%')[0])
        # Calculate the estimated minute based on the position percentage
        if current_minute < starting_minute_second_half:
            estimated_minute = int((position_percentage / 100) * starting_minute_second_half) + 1
        else:
            # Calculate the estimated minute for the second half
            estimated_minute = starting_minute_second_half + int((position_percentage / 100) * (total_duration_minutes - starting_minute_second_half))
        # Check if the estimated minute exceeds the initial total duration
        if estimated_minute > total_duration_minutes:
            # Update the total duration and record any additional time
            additional_time += estimated_minute - total_duration_minutes
            total_duration_minutes = estimated_minute
        # Get the class attribute
        class_name = event_icon.get_attribute('class')
        # Extract event type (e.g., Goal, YellowCard, etc.)
        event_type = class_name.split()[1]  # Assuming the second class name represents the event type
        # Extract home/away information
        home_or_away = class_name.split()[2]  # Assuming the third class name represents home/away
        # Write the event type, home/away, and estimated minute to the file
        if additional_time > 0 and estimated_minute > total_duration_minutes:
            file.write(f"{event_type} {home_or_away}- {total_duration_minutes}+{additional_time}'\n")
        else:
            file.write(f"{event_type} {home_or_away}- {estimated_minute}'\n")
        # Increment the current minute
        current_minute = estimated_minute

     # Write the embedded PNG image path to the text file
    file.write('\n\nEmbedded PNG Image:\n')
    file.write(screenshot_path)

time.sleep(3)

# Find the menu by its id and click on it
menu_button = driver.find_element(By.ID, 'menu')
menu_button.click()

time.sleep(2)
# Define the path to the text file
file_path = f'{folder_name}/info_{event_name}.txt'

# Initialize variables to track the score
home_score = 0
away_score = 0

# Initialize a list to store goal events
goals = []

# Open the text file in read mode
with open(file_path, 'r') as file:
    # Read all lines from the file
    lines = file.readlines()

    # Iterate through each line
    for line in lines:
        # Check if the line contains "Goal" information
        if "Goal" in line:
            # Split the line by whitespace
            parts = line.strip().split()
            event_type = parts[0]  # Extract event type
            home_or_away = parts[1]  # Extract home/away information
            minute = parts[-1][:-1]  # Extract minute information

             # Store the goal event in the list
            goals.append((home_or_away, minute))

            # Update the score based on the team
            if event_type == "Goal":
                if "home" in home_or_away:
                    home_score += 1
                elif "away" in home_or_away:
                    away_score += 1

# Print the final scores
print(f"Final Score: {home_score}-{away_score}")

# Print all the goals sequentially
for i, goal in enumerate(goals, start=1):
    home_or_away, minute = goal
    print(f"Goal {i}: {home_or_away} team scored at {minute}. minute")


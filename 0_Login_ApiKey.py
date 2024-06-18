#Open historical data (API) page and using my username and password to login 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuration of the Chrome webdriver
options = webdriver.ChromeOptions()

# Initialize the Chrome webdriver
driver = webdriver.Chrome(options=options)

# Navigate to the specified URL
driver.get('https://historicdata.betfair.com/#/home')

# Find the username input field and enter the username
username_input = driver.find_element(By.XPATH, '//input[@placeholder="E-mail/Username"]')
username_input.send_keys('allisonrmartin')

# Find the password input field and enter the password
password_input = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_input.send_keys('313577Pl,.')

# Find and click the login button
login_button = driver.find_element(By.CSS_SELECTOR, 'input.login-button')
login_button.click()

#After logging in, go to obtain app_key and ssoid
# Navigate to the specified URL
driver.get('https://docs.developer.betfair.com/visualisers/api-ng-account-operations/')

# Find the session token input field and obtain its value
session_token_input = driver.find_element(By.ID, 'sessionToken-inputEl')
session_token = session_token_input.get_attribute('value')
print("Session Token (ssoid):", session_token)



# Click on the "getDeveloperAppKeys" button
get_app_keys_button = driver.find_element(By.XPATH, '//div[text()="getDeveloperAppKeys"]')
get_app_keys_button.click()
# Click on the "Execute" button
execute_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, 'button-1041-btnIconEl'))
)
execute_button.click()
# Click on the "+" button to expand the row
plus_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CLASS_NAME, 'x-grid-row-expander'))
)
plus_button.click()


# Increase timeout if needed
wait = WebDriverWait(driver, 20)

# Wait for the visibility of the element with specific id and class
td_element = wait.until(EC.visibility_of_element_located((By.XPATH, '//td[@id="ext-gen1186" and contains(@class, "x-grid-cell-gridcolumn-1046")]')))

# Once the element is visible, extract the text
app_key = td_element.text

# Print the extracted text
print("Application Key:", app_key)

driver.quit()

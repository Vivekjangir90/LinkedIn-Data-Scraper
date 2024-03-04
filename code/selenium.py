from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time



# Initialize Chrome WebDriver
driver = webdriver.Chrome()

# Navigate to LinkedIn
driver.get('https://www.linkedin.com/search/results/people/?firstName=Vivek&lastName=Jangir&origin=SEO_PSERP&sid=sn_')

# Find username and password fields
wait = WebDriverWait(driver, 10)
signin_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'main__sign-in-link')))
signin_link.click()
time.sleep(3)

username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')

# Input username and password
username.send_keys('vivekjangir90+lnkd@gmail.com')
password.send_keys('Vivek#9024')
time.sleep(1)
# login_link = driver.find_element(By.CLASS_NAME , 'login__form_action_container')

login_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
login_link.click()

time.sleep(5)
# login_link1 = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'reusable-search__result-container')))
# login_link1.click()
# print("That is my first url : \n", login_link1)
# Wait for the page to fully load after login
# wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'reusable-search__result-container')))

# Find all search result containers
search_result_containers = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
# print(search_result_containers)
# print(driver.current_url)
username = []
for container in search_result_containers:
    # Find the anchor element within the container
    anchor_element = container.find_element(By.TAG_NAME, 'a')
    
    # Get the value of the 'href' attribute
    url = anchor_element.get_attribute('href')

    parts = url.split("/in/", 1)
    username = parts[1].split("?")[0].strip()
    usernames.append(username)


# Close the browser
driver.quit()


# LinkedIn URL
# url = "https://www.linkedin.com/search/results/people/?firstName=Vivek&lastName=Jangir&origin=SEO_PSERP&sid=sn_"
# print("5")

# # # Open the URL
# driver.get(url)
# print("6")
# time.sleep(100)

# last_height = driver.execute_script("return document.body.scrollHeight")
# while True:
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(2)  # Adjust the sleep time as needed
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

# # Wait for a short time to ensure all content is loaded
# time.sleep(5)

# Get the page source after dynamic content has loaded
# page_source = driver.page_source

# Use BeautifulSoup to parse the page source
# soup = BeautifulSoup(page_source, "html.parser")
# print(soup)
# Find the title and body elements
# title = soup.title
# body = soup.body

# Print the title and body (or do further processing)
# print("Title:", title.text)
# print("Body:", body.text)

# Close the WebDriver
# driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_api import Linkedin
import pandas as pd
import time


# Input username and password
client_user_name = str(input("Enter your LinkedIn username or Email address : "))
client_user_password = str(input("Enter your LinkedIn Password : "))

print("\n\nHello! \n\nEnter the name for which you want to retrieve details.\n\n")
find_user_first_name = str(input("Enter first name : "))
find_user_last_name = str(input("Enter last name : "))

# open Chrome WebDriver
driver = webdriver.Chrome()
url = f'https://www.linkedin.com/search/results/people/?firstName={find_user_first_name}&lastName={find_user_last_name}&origin=SEO_PSERP&sid=sn_'
# find user in LinkedIn
driver.get(url)

# Find username and password fields
wait = WebDriverWait(driver, 10)
signin_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'main__sign-in-link')))
signin_link.click()
time.sleep(1)

username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')

username.send_keys(client_user_name)
password.send_keys(client_user_password)
time.sleep(1)

login_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
login_link.click()
time.sleep(5)

# Find all search result(only  username)
usernames = []
search_result_containers = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')

for container in search_result_containers:
    try:
        anchor_element = container.find_element(By.TAG_NAME, 'a')
        url = anchor_element.get_attribute('href')
        parts = url.split("/in/", 1)
        username = parts[1].split("?")[0].strip()
        usernames.append(username)
        print(container)
    except:
        print("sorry")
driver.quit()

# Create an empty DataFrame
df = pd.DataFrame(columns=["FULL NAME", "FIRST NAME", "LAST NAME", "USERNAME",
                            "LOCATION", "COUNTRY", "SKILLS", "FOLLOWERS", "CONNECTIONS", 
                            "EXPERIENCE", "PROFILE IMAGE", "SUMMARY", "LAST POST URL", "LAST POST CONTENT"])
print(usernames)
for user in usernames:
    print(user)
    # Use LinkedIn-api library
    api = Linkedin(client_user_name, client_user_password)

    # GET a profile
    profile = api.get_profile(user)

    useful_details = []
    for item in profile['experience']:
        try:
            details = {}
            details['Location'] = item['locationName']
            details['Company Name'] = item['companyName']
            details['Title'] = item['title']
            details['Start Date'] = f"{item['timePeriod']['startDate']['month']}-{item['timePeriod']['startDate']['year']}"
            if 'endDate' in item['timePeriod']:
                details['End Date'] = f"{item['timePeriod']['endDate']['month']}-{item['timePeriod']['endDate']['year']}"
            if 'industries' in item['company']:
                details['Industry'] = item['company']['industries'][0]
            useful_details.append(details)
        except Exception as e:
            pass
    # for i in useful_details:
    #     print(i)   

    profile_net_info = api.get_profile_network_info(user)

    skills = []
    profile_skills = api.get_profile_skills(public_id=user)
    for i in profile_skills:
        # print(i['name'])
        skills.append(i['name'])

    profile_posts = api.get_profile_posts(public_id=user,post_count=1)

    try:
        full_name =  profile['firstName']+" "+profile['lastName']
    except:
        full_name = "null"
    try:
        firstName = profile['firstName']
    except:
        firstName = "null"
    try:
        lastName = profile['lastName']
    except:
        lastName = "null"
    try:
        public_id = profile['public_id']
    except:
        public_id = "null"
    try:
        geoLocationName = profile['geoLocationName']
    except:
        geoLocationName = "null"
    try:
        geoCountryName = profile['geoCountryName']
    except:
        geoCountryName = "null"
    try:
        followersCount = profile_net_info['followersCount']
    except:
        followersCount = "null"
    try:
        connectionsCount = profile_net_info['connectionsCount']
    except:
        connectionsCount = "null"
    try:
        displayPictureUrl = profile['displayPictureUrl'] + profile['img_500_500']
    except:
        displayPictureUrl = "null"
    try:
        summary = profile['summary']
    except:
        summary = "null"
    try:
        profile_posts_url = profile_posts[0]['updateMetadata']['updateActions']['actions'][1]['url']
    except:
        profile_posts_url = "null"
    try:
        profile_posts_content = profile_posts[0]['commentary']['text']['text']
    except:
        profile_posts_content = "null"
    # Append data to the DataFrame
    row_data =  {
        "FULL NAME": full_name,
        "FIRST NAME": firstName,
        "LAST NAME": lastName,
        "USERNAME": public_id,
        "LOCATION": geoLocationName,
        "COUNTRY": geoCountryName,
        "SKILLS": skills,
        "FOLLOWERS": followersCount,
        "CONNECTIONS": connectionsCount,
        "EXPERIENCE": useful_details,
        "PROFILE IMAGE": displayPictureUrl,
        "SUMMARY": summary,
        "LAST POST URL": profile_posts_url,
        "LAST POST CONTENT": profile_posts_content
        }

    # Append row_data to the DataFrame
    df = df._append(row_data, ignore_index=True)

file_name = find_user_first_name +" "+ find_user_last_name
df.to_csv(f"{file_name}.csv", index=False)
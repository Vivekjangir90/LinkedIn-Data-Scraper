from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from linkedin_api import Linkedin
import pandas as pd

def get_usernames(driver):
    search_result_containers = driver.find_elements(By.CLASS_NAME, 'reusable-search__result-container')
    usernames = []
    for container in search_result_containers:
        try:
            anchor_element = container.find_element(By.TAG_NAME, 'a')
            url = anchor_element.get_attribute('href')
            parts = url.split("/in/", 1)
            username = parts[1].split("?")[0].strip()
            usernames.append(username)
        except Exception as e:
            print("Error while extracting username:", e)
    return usernames

def get_profile_data(api, user):
    try:
        profile = api.get_profile(user)
        profile_net_info = api.get_profile_network_info(user)
        profile_skills = [i['name'] for i in api.get_profile_skills(public_id=user)]
        profile_posts = api.get_profile_posts(public_id=user, post_count=1)
    except:
        print("Couldn't find \nPlease try again!")
    useful_details = []
    full_name = profile.get('firstName', '') + " " + profile.get('lastName', '')
    personal_data = {
        "FULL NAME": full_name,
        "FIRST NAME": profile.get('firstName', ''),
        "LAST NAME": profile.get('lastName', ''),
        "USERNAME": user,
        "LOCATION": profile.get('geoLocationName', ''),
        "COUNTRY": profile.get('geoCountryName', ''),
        "SKILLS": profile_skills,
        "FOLLOWERS": profile_net_info.get('followersCount', ''),
        "CONNECTIONS": profile_net_info.get('connectionsCount', ''),
        "EXPERIENCE": useful_details,
        "PROFILE IMAGE": profile.get('displayPictureUrl', '') + profile.get('img_500_500', ''),
        "SUMMARY": profile.get('summary', ''),
        
    }
    try:
        LAST_POST_URL = profile_posts[0]['updateMetadata']['updateActions']['actions'][1]['url'] if profile_posts else ''
        LAST_POST_CONTENT = profile_posts[0]['commentary']['text']['text'] if profile_posts else ''
        personal_data.update({"LAST POST URL": LAST_POST_URL, "LAST POST CONTENT": LAST_POST_CONTENT})
    except Exception as e:
            print("Error while extracting experience details:", e)

    for item in profile.get('experience', []):
        try:
            details = {
                'Location': item.get('locationName', ''),
                'Company Name': item.get('companyName', ''),
                'Title': item.get('title', ''),
                'Start Date': f"{item['timePeriod']['startDate']['month']}-{item['timePeriod']['startDate']['year']}",
                'End Date': f"{item['timePeriod']['endDate']['month']}-{item['timePeriod']['endDate']['year']}" if 'endDate' in item['timePeriod'] else '',
                'Industry': item['company']['industries'][0] if 'industries' in item['company'] else ''
            }
            useful_details.append(details)
        except Exception as e:
            print("Error while extracting experience details:", e)
    return personal_data
    


client_user_name = input("Enter your LinkedIn username or Email address: ")
client_user_password = input("Enter your LinkedIn Password: ")
find_user_first_name = input("Enter first name: ")
find_user_last_name = input("Enter last name: ")

driver = webdriver.Chrome()
driver.get(f'https://www.linkedin.com/search/results/people/?firstName={find_user_first_name}&lastName={find_user_last_name}&origin=SEO_PSERP&sid=sn_')

wait = WebDriverWait(driver, 10)
signin_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'main__sign-in-link')))
signin_link.click()

username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password')

username.send_keys(client_user_name)
password.send_keys(client_user_password)

login_link = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'login__form_action_container')))
login_link.click()

usernames = get_usernames(driver)
driver.quit()

df = pd.DataFrame(columns=["FULL NAME", "FIRST NAME", "LAST NAME", "USERNAME", "LOCATION", "COUNTRY", "SKILLS", "FOLLOWERS", "CONNECTIONS", "EXPERIENCE", "PROFILE IMAGE", "SUMMARY", "LAST POST URL", "LAST POST CONTENT"])

api = Linkedin(client_user_name, client_user_password)


for user in usernames:
    row_data = get_profile_data(api, user)
    df = df._append(row_data, ignore_index=True)

file_name = find_user_first_name + " " + find_user_last_name
df.to_csv(f"{file_name}.csv", index=False)

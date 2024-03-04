from linkedin_api import Linkedin
import pandas as pd

# Authenticate using any Linkedin account credentials
api = Linkedin('presidential918@desertsundesigns.com', 'presidential918@d')

# GET a profile
profile = api.get_profile('vivek-jangir-1b5b17259')
# print(profile)

# GET a profiles contact info
contact_info = api.get_profile_contact_info('vivek-jangir-1b5b17259')
# print(contact_info)


# GET 1st degree connections of a given profile
# connections = api.get_profile_connections('vivek-jangir-1b5b17259')
# print(profile['firstName'],"",profile['lastName'])
# print(profile['geoLocationName'])
# print(profile['geoCountryName'])
# print(profile['displayPictureUrl'] + profile['img_400_400'])
# print(profile['public_id'])
# print(profile['profile_id'])
# print(profile['summary'])

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

profile_net_info = api.get_profile_network_info('vivek-jangir-1b5b17259')

# print(profile_net_info['followersCount'])
# print(profile_net_info['connectionsCount'])

# profile_badges = api.get_profile_member_badges('yuvraj8')
# print(profile_badges,"\n")

# profile_privacy = api.get_profile_privacy_settings('yuvraj8')
# print(profile_privacy,"\n")

# profile_updates = api.get_profile_updates(public_id='yuvraj8', max_results=5)
# print(profile_updates,"\n")

skills = []
profile_skills = api.get_profile_skills(public_id='vivek-jangir-1b5b17259')
for i in profile_skills:
    print(i['name'])
    skills.append(i['name'])

profile_posts = api.get_profile_posts(public_id='vivek-jangir-1b5b17259',post_count=1)
# print(profile_posts[0]['updateMetadata']['updateActions']['actions'][1]['url'],'\n')
# print(profile_posts[0]['commentary']['text']['text'],'\n')
# print(profile_posts[1]['updateMetadata']['updateActions']['actions'][1]['url'],'\n')
# print(profile_posts[1]['commentary']['text']['text'],'\n')



# Create an empty DataFrame
df = pd.DataFrame(columns=["FULL NAME", "FIRST NAME", "LAST NAME", "USERNAME",
                            "LOCATION", "COUNTRY", "SKILLS", "FOLLOWERS", "CONNECTIONS", 
                            "EXPERIENCE", "PROFILE IMAGE", "SUMMARY", "LAST POST URL", "LAST POST CONTENT"])

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
df.to_csv("output.csv", index=False)
import requests
import os
import json

# import config file with Buzzsprout podcast id and api key
with open('config.json', 'r') as file:
    content = file.read()
    if not content:
        print("The file is empty")
    else:
        config = json.loads(content)

# set variables from config file
buzzsprout_api_key = config['database']['buzzsprout_api_key']
podcast_id = config['database']['podcast_id']
url = "https://www.buzzsprout.com/api/" + podcast_id + "/episodes.json"

# print episodes from api
headers = {
    "Authorization": buzzsprout_api_key
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    episodes = response.json()
    # Process the episodes data here
    for episode in episodes:
        print(episode)
else:
    print("Failed to retrieve episodes. Status code:", response.status_code)
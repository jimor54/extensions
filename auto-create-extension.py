import requests
import json

url = "https://raw.githubusercontent.com/keiyoushi/extensions/repo/index.min.json"
response = requests.get(url)

if response.status_code != 200:
    print(f"Failed to fetch data. Status code: {response.status_code}")
    exit()

json_data = response.json()

list_without_nsfw = []

for data in json_data:
    if 'nsfw' not in data or data['nsfw'] == 0:
        list_without_nsfw.append(data)

with open("index.min.json", "w") as file:
    json.dump(list_without_nsfw, file)

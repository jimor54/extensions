import requests
import json
import zipfile
import shutil
import os

## IMPORT AND MODIFY INDEX.MIN.JSON FILE
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

## IMPORT APK AND ICON FILE

repo_url = 'https://github.com/keiyoushi/extensions/archive/refs/heads/repo.zip'
zip_file = 'extensions_repo.zip'

response = requests.get(repo_url)

# Save the ZIP file locally
with open(zip_file, 'wb') as file:
    file.write(response.content)

# Step 2: Extract the ZIP file
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall('extracted_repo')

# Step 3: Define the source paths for 'apk' and 'icon' folders from the extracted content
extracted_folder = 'extracted_repo/extensions-repo'
apk_src = os.path.join(extracted_folder, 'apk')
icon_src = os.path.join(extracted_folder, 'icon')

# Step 4: Define destination directories in the root of the current working directory
apk_dest = os.path.join(os.getcwd(), 'apk')
icon_dest = os.path.join(os.getcwd(), 'icon')

# Step 5: Copy the 'apk' and 'icon' directories to the root
if os.path.exists(apk_src):
    shutil.copytree(apk_src, apk_dest, dirs_exist_ok=True) 
    print(f"'apk' folder copied successfully to {apk_dest}")
else:
    print("'apk' folder not found.")

if os.path.exists(icon_src):
    shutil.copytree(icon_src, icon_dest, dirs_exist_ok=True)
    print(f"'icon' folder copied successfully to {icon_dest}")
else:
    print("'icon' folder not found.")

# Optional: Clean up the downloaded ZIP file and extracted folder
os.remove(zip_file)
shutil.rmtree('extracted_repo')

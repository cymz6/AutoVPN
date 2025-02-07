import base64
import requests
import os
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

# Download list.txt from GitHub
//list_url = "https://raw.githubusercontent.com/peasoft/NoMoreWalls/master/list.txt"
list_url = "https://raw.githubusercontent.com/cymz6/NoMoreWalls/refs/heads/master/list.txt"
response = requests.get(list_url)
with open("list.txt", "wb") as file:
    file.write(response.content)

# Read and decode list.txt
with open("list.txt", "r") as file:
    content = file.read()
decoded_content = base64.b64decode(content).decode('utf-8')

# Filter out lines starting with "http"
filtered_lines = [line for line in decoded_content.split('\n') if not line.startswith("http")]
encoded_content = base64.b64encode('\n'.join(filtered_lines).encode('utf-8')).decode('utf-8')

# Create data directory if it doesn't exist
if not os.path.exists("data"):
    os.makedirs("data")

# Save the encoded content to V2 files
with open("V2", "w") as file:
    file.write(encoded_content)
with open("data/V2.txt", "w") as file:
    file.write(encoded_content)

# Get current system time and save it to UpdateTime.txt
time_url = "https://quan.suning.com/getSysTime.do"
time_response = requests.get(time_url)
script_execution_time = time_response.text

with open("data/UpdateTime.txt", "w") as file:
    file.write(script_execution_time)

# Get current date and create a zip file for the data directory
current_date = datetime.now().strftime("%Y%m%d")
zip_filename = f"{current_date}.zip"

# Create a zip file of the data directory
with ZipFile(zip_filename, 'w', ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('data'):
        for file in files:
            full_path = os.path.join(root, file)
            zipf.write(full_path, os.path.relpath(full_path, 'data'))

# Move the zip file to the databak directory
databak_dir = 'databak'
if not os.path.exists(databak_dir):
    os.makedirs(databak_dir)
zip_dest = os.path.join(databak_dir, zip_filename)
os.rename(zip_filename, zip_dest)

print(f"Zip file '{zip_dest}' created successfully.")

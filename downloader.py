import os
import requests
from bs4 import BeautifulSoup
import time

OUTPUT_DIRECTORY = "./flags"
URL = "https://www.worldometers.info"
REQUEST_COOLDOWN = 0.5

# Check if output directory exists; if it does, do nothing
if not os.path.exists(OUTPUT_DIRECTORY):
    os.mkdir(path=OUTPUT_DIRECTORY)

# Get flag grid
response = requests.get(f'{URL}/geography/flags-of-the-world/')
soup = BeautifulSoup(response.text, "html.parser")
list_entries = soup.find("div", {"class": "content-inner"}).find("div", {"class": "row"}).find_all("div", {"class": "col-md-4"})

# Loop through all items in grid
for entry in list_entries:
    flag_container = entry.find("div")
    country_name = entry.find("div").text
    flag_src = flag_container.find("img")["src"]
    image = requests.get(URL + flag_src)
    
    # Create new image file
    with open(OUTPUT_DIRECTORY + "/" + flag_src.split("/")[-1].replace("tn_", "").replace("-flag", ""), 'wb') as f:
        f.write(image.content)
    
    print(f'Created file for {country_name}: {OUTPUT_DIRECTORY}/{flag_src.split("/")[-1].replace("tn_", "").replace("-flag", "")}')
    time.sleep(REQUEST_COOLDOWN)
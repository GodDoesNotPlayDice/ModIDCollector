# Create by God Does Not Play Dice

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
import subprocess

chromedriver_autoinstaller.install()
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
print("""
  ______    _                                 ______         __   __                _    _                           _____  ______    
.' ____ \  / |_                             .' ___  |       [  | [  |              / |_ (_)                         |_   _||_   _ `.  
| (___ \_|`| |-'.---.  ,--.   _ .--..--.   / .'   \_|  .--.  | |  | | .---.  .---.`| |-'__   .--.   _ .--.   .--.     | |    | | `. \ 
 _.____`.  | | / /__\\`'_\ : [ `.-. .-. |  | |       / .'`\ \| |  | |/ /__\\/ /'`\]| | [  |/ .'`\ \[ `.-. | ( (`\]    | |    | |  | | 
| \____) | | |,| \__.,// | |, | | | | | |  \ `.___.'\| \__. || |  | || \__.,| \__. | |, | || \__. | | | | |  `'.'.   _| |_  _| |_.' / 
 \______.' \__/ '.__.'\'-;__/[___||__||__]  `.____ .' '.__.'[___][___]'.__.''.___.'\__/[___]'.__.' [___||__][\__) ) |_____||______.'  
      
1.) Enter ur Steam collection URL
2.) Enter the name of the file where the IDs will be saved.
                                                             
""")

def check_url_availability(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"La URL {url} is available.")
            return True
        else:
            print(f"La URL {url} it's not available. : {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"No se pudo acceder a la URL {url}. Error: {e}")
        return False


try:
    while True:
        web_path = str(input("Enter the Steam collection: "))
        if web_path == "":
            print("\nPlease enter a valid URL")
            continue
        else:
            break
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
except Exception as e:
    print(f"\nError: {e}")
    print("Please enter a valid URL")

if check_url_availability(web_path):
    try:
        name_file = str(input("Enter the name of the file where the IDs will be saved: "))
        if name_file == "":
            raise ValueError("Invalid file name")
        driver.get(web_path)
        elements = driver.find_elements(by=By.CLASS_NAME, value="collectionItem")
        ids = []
        for e in elements:
            element_id = e.get_attribute("id")
            if element_id:
                ids.append(element_id.replace("sharedfile_", ""))
        
        if ids:
            with open(f'./{name_file}.txt', 'a+') as file:
                for item in ids:
                    file.write(str(item) + '\n')
            print(f"IDs saved in '{name_file}.txt'")
        else:
            print("No elements found in the collection.")
        
        driver.quit()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nError: {e}")
else:
    print("No valid URL entered. Exiting...")
    
subprocess.call("cmd.exe", shell=True)
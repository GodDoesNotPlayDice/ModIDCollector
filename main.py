# Create by God Does Not Play Dice

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
import requests
import subprocess
import re
import os

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
        print(f"It was not possible to access the {url}. Error: {e}")
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
        mod_ids = []
        path_not_found = []
        for e in elements:
            element_id = e.get_attribute("id")
            if element_id:
                ids.append(element_id.replace("sharedfile_", ""))
        found = 0
        loss = 0
        count = 0
        total = len(ids)
        for id in ids:
            web_path = f"https://steamcommunity.com/sharedfiles/filedetails/?id={id}"
            driver.get(web_path)
            element = driver.find_element(by=By.XPATH, value='//div[@class="workshopItemDescription" and @id="highlightContent"]')
            rex = r"Mod ID:\s*(.+)"
            res = re.search(rex, element.text)

            if res:
                print(f"ID: {res.group(1)} FOUND IN {web_path}")
                mod_id = res.group(1)
                mod_ids.append({'mod_id': mod_id, 'id': id})

                found += 1
            else:
                print(f"ID NOT FOUND IN {web_path}")
                mod_id = "NOT FOUND"
                path_not_found.append(web_path)
                loss += 1

            print(mod_id)
            count += 1
            print(f"Found: {found}")
            print(f"Loss: {loss}")
            print(f"Total: {count}/{total}")

        if (count - loss) == total:
            os.system('cls')
            print(f"Found: {found}")
            print(f"Loss: {loss}")
            print(f"Total: {count}/{total}")
            print("Success! All IDs have been found.")

        else:
            os.system('cls')
            print("-----------------------------------")
            print("Not success! Some IDs have not been found.")
            print("Try to check your mods in the collection and try again.")
            print("---------------Warning-----------------\n")
            print(f"Found: {found}")
            print(f"Loss: {loss}")
            print(f"Total: {count - loss}/{total}")
            print("Paths not found:")
            for path in path_not_found:
                print(path)
        
        if mod_ids:
            with open(f'./{name_file}.txt', 'a+') as file:
                index = 0
                for mod in mod_ids:
                    file.write(f"Workshop ID: {mod['id']}\nMod ID: {mod['mod_id']}\n")
                    index += 1
            print("\nSaved Only success mods IDs in the file.")
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
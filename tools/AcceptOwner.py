from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import warnings
from colorama import Fore, init
import sys
import time

init(convert=True)

warnings.filterwarnings("ignore")

user_data_dir = "PATH_TO_CHROME_USER_DATA_DIRECTORY"
profile = "PROFILE NAME"
delay = 0.1

input(f"{Fore.MAGENTA}Chrome profile: {Fore.YELLOW}{profile}{Fore.MAGENTA}, press ENTER to close all chrome processes and start...")
os.system('taskkill /F /IM "chrome.exe" /T')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile}")
driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get(f"https://myaccount.google.com/u/0/brandaccounts")
input("Choose the right google account, navigate to invites, press ENTER to continue...")
elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/accept')]")
invites = [elem.get_attribute('href') for elem in elements]
input(f"Found {len(invites)} invites, press ENTER to continue...")
counter = 0
for invite in invites:
    counter = counter + 1
    driver.get(invite)
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz/div/div[2]/div[2]/div/div[3]/c-wiz/div[4]/div/span/span"))).click()
        for i in range(20):
            time.sleep(0.5)
            if "/view" in driver.current_url:
                time.sleep(delay)
                break
            if i == 19:
                input("TIMEOUT, FIX MANUALLY and press ENTER to continue to next one...")
    except:
        input("ERROR, FIX MANUALLY and press ENTER to continue to next one...")
    print(f"{Fore.MAGENTA}Accepted invite {counter}")

driver.quit()
input(f"{Fore.LIGHTGREEN_EX}Accepted all invites, press ENTER to close...")
sys.exit()
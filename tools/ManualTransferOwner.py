from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import os
import warnings
from colorama import Fore, init
import sys
import time

init(convert=True)

warnings.filterwarnings("ignore")

user_data_dir = "PATH_TO_CHROME_USER_DATA_DIRECTORY"
profile = "PROFILE NAME"
transfer_tos = ["EMAIL@gmail.com", "EMAIL@gmail.com", "EMAIL@gmail.com"]
delay = 0.1

input(f"{Fore.MAGENTA}Chrome profile: {Fore.YELLOW}{profile}{Fore.MAGENTA}, press ENTER to close all chrome processes and start...")
os.system('taskkill /F /IM "chrome.exe" /T')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile}")
driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get(f"https://myaccount.google.com/brandaccounts")
input(f"Authenticate once, press ENTER to continue...")
elements = driver.find_elements(By.CLASS_NAME, "zwGcVb")
brand_accounts = [elem.get_attribute('href') for elem in elements]
del brand_accounts[0]
rapt = driver.current_url.split("?rapt=")[-1]
input(f"Found {len(brand_accounts)} brand accounts, rapt: ({rapt}), press ENTER to continue...")
counter = 0
for brand_account in brand_accounts:
    counter = counter + 1
    driver.get(f"{brand_account}?rapt={rapt}")
    username = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "DUoEXc"))).text
    time.sleep(0.5)
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(f"https://www.youtube.com/user/{username}/about")
    transfer_to = transfer_tos[int(input("What account? (0,1,2,3): "))]
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Manage permissions')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Primary owner')]")))
        time.sleep(delay)
        add_user = driver.find_elements(By.CLASS_NAME, "DPvwYc")[-1]
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((add_user))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Add new users')]")))
        time.sleep(delay)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[2]/span/div/c-wiz/div/div[1]/input[2]"))).send_keys(transfer_to)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[2]/span/div/c-wiz/div/div[1]/input[2]"))).send_keys(Keys.ENTER)
        time.sleep(delay)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[2]/span/div/div/div[1]/div[1]/div[1]"))).click()
        time.sleep(delay)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[12]/div/div[2]/span/div/div/div[2]/div[2]"))).click()
        time.sleep(delay)
        invite_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Invite')]")[-1]
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((invite_button))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Invited, Owner')]")))
        time.sleep(delay)
        done_button = driver.find_elements(By.XPATH, "//*[contains(text(), 'Done')]")[-1]
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((done_button))).click()
        time.sleep(delay)
    except:
        input("ERROR, FIX MANUALLY and press ENTER to continue to next one...")
        rapt = driver.current_url.split("?rapt=")[-1]
    print(f"{Fore.MAGENTA}Invited {Fore.YELLOW}{transfer_to}{Fore.MAGENTA} as owner for ({counter}) {Fore.YELLOW}{username}{Fore.MAGENTA}")

driver.quit()
input(f"{Fore.LIGHTGREEN_EX}Invited {transfer_to} for all channels, press ENTER to close...")
sys.exit()
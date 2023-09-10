from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import warnings
import json
from colorama import Fore, init
import sys

init(convert=True)

warnings.filterwarnings("ignore")

user_data_dir = "PATH_TO_CHROME_USER_DATA_DIRECTORY"
profile = "PROFILE NAME"

input(f"{Fore.MAGENTA}Chrome profile: {Fore.YELLOW}{profile}{Fore.MAGENTA}, make sure that the first google account is selected in youtube, press ENTER to close all chrome processes and start...")
os.system('taskkill /F /IM "chrome.exe" /T')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument(f"user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory={profile}")
driver = webdriver.Chrome("chromedriver.exe", options=options)
driver.get("https://www.youtube.com/gaia_link")
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "avatar-btn"))).click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]"))).click()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[2]")))
account_channels = driver.find_elements(By.CLASS_NAME, "style-scope ytd-account-item-section-renderer")
print(f"Found {len(account_channels)} logged in google accs")
for i in range(len(account_channels)):
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[4]/ytd-multi-page-menu-renderer/div[3]/div[1]/ytd-account-section-list-renderer[{i+1}]/div[2]/ytd-account-item-section-renderer/div[2]/ytd-account-item-renderer[1]"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[1]/ytd-item-section-header-renderer/div[1]/div")))
    driver.get("https://www.youtube.com/gaia_link")
    email = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-page-introduction-renderer/div[1]/div/yt-formatted-string[1]/span[3]"))).text
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-settings-options-renderer/div/div[2]/div/ytd-settings-gaia-link-renderer/div/div[1]/yt-form-renderer/div/yt-text-input-form-field-renderer[1]/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input"))).send_keys("Aladwa")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-settings-options-renderer/div/div[2]/div/ytd-settings-gaia-link-renderer/div/div[1]/yt-form-renderer/div/yt-text-input-form-field-renderer[2]/tp-yt-paper-input/tp-yt-paper-input-container/div[2]/div/iron-input/input"))).send_keys("Aladwa")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[2]/div[3]/ytd-settings-options-renderer/div/div[2]/div/ytd-settings-gaia-link-renderer/div/div[2]/ytd-button-renderer"))).click()
    request = driver.wait_for_request('https://www.youtube.com/youtubei/v1/channel/claim_legacy_youtube_channel')
    authorization = request.headers['authorization']
    cookie = request.headers['cookie']
    x_goog_visitor_id = request.headers['x-goog-visitor-id']
    x_goog_authuser = request.headers['x-goog-authuser']
    del driver.requests
    headers = {
			"email": f"{email}",
			"authorization": f"{authorization}",
			"cookie": f"{cookie}",
			"x-goog-visitor-id": f"{x_goog_visitor_id}",
			"x-goog-authuser": f"{x_goog_authuser}"
		}
    with open(f"{profile}.json", "a", encoding="utf-8") as file:
        file.write(json.dumps(headers, indent=4))
        if not i == len(account_channels)-1:
            file.write(",\n")
    print(f"{Fore.MAGENTA}Saved headers of account ({Fore.YELLOW}{i+1}{Fore.MAGENTA}) ({Fore.YELLOW}{email}{Fore.MAGENTA})")
    if i == len(account_channels)-1:
        driver.quit()
    else:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "avatar-btn"))).click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/ytd-app/ytd-popup-container/tp-yt-iron-dropdown/div/ytd-multi-page-menu-renderer/div[3]/div[1]/yt-multi-page-menu-section-renderer[1]/div[2]/ytd-compact-link-renderer[3]"))).click()

input(f"{Fore.LIGHTGREEN_EX}Saved all, press ENTER to close...")
sys.exit()
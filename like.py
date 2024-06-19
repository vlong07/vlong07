
import re
import requests
from bs4 import BeautifulSoup
import os
import sys
import hashlib


# File to track user sessions
USER_SESSION_FILE = 'key.txt'

session = requests.Session()

def isnumeric(value):
    try:
        return str(value).isnumeric()
    except:
        return False

def check_login(cookie):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "upgrade-insecure-requests": "1",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-dest": "document",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cookie": cookie
    }
    response = session.get("https://dvmxh.azdigi.blog", headers=headers).text
    
    if "setTimeout(function(){ location.href = '/login' },0);" in response:
        return (False, None, None)
    elif "Đăng Xuất" in response:
        return (True, cookie, response)
    else:
        return (False, None, None)

def get_info(html):
    soup = BeautifulSoup(html, "html.parser")
    username_element = soup.find("h5", class_="gradient-text")
    if username_element:
        username_parts = username_element.text.split("|")
        username = username_parts[0].strip()
        amount = username_parts[1].strip() if len(username_parts) > 1 else "Không tìm thấy"
    else:
        username = "Không tìm thấy"
        amount = "Không tìm thấy"
    
    return username, amount

def get_server(cookie):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "upgrade-insecure-requests": "1",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://dvmxh.azdigi.blog/",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cookie": cookie
    }
    response = session.get("https://dvmxh.azdigi.blog/facebook/likev2.php", headers=headers).text
    soup = BeautifulSoup(response, "html.parser")
    servers = [label.text.strip() for label in soup.find_all("label", class_="form-check-label")]
    
    return "\n".join(servers) if servers else "Không thể lấy thông tin server!"

def buy_like(cookie, id_post, server, amount):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "cache-control": "max-age=0",
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": "\"Android\"",
        "upgrade-insecure-requests": "1",
        "origin": "https://dvmxh.azdigi.blog",
        "sec-fetch-site": "same-origin",
        "sec-fetch-mode": "navigate",
        "sec-fetch-user": "?1",
        "sec-fetch-dest": "document",
        "referer": "https://dvmxh.azdigi.blog/facebook/likev2.php",
        "accept-language": "vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
        "Cookie": cookie
    }
    
    payload = {
        "id": id_post,
        "server_order": "sv" + str(server),
        "sl": int(amount),
        "submit": ""
    }
    
    response = session.post("https://dvmxh.azdigi.blog/facebook/likev2.php", headers=headers, data=payload)
    
    return response.text

def get_response(html):
    soup = BeautifulSoup(html, "html.parser")
    script_tag = soup.find("script", type="text/javascript")
    js_code = script_tag.text if script_tag else ""
    
    pattern = r"message: \"(.*?)\""
    
    try:
        match = re.search(pattern, js_code)
        message = match.group(1)
        return message
    except AttributeError:
        return "Không tìm thấy trạng thái mua like!"

def load_user_sessions():
    if os.path.exists(USER_SESSION_FILE):
        with open(USER_SESSION_FILE, 'r') as file:
            return set(line.strip() for line in file.readlines())
    return set()

def save_user_session(session_hash):
    with open(USER_SESSION_FILE, 'a') as file:
        file.write(f"{session_hash}\n")

def hash_cookie(cookie):
    return hashlib.sha256(cookie.encode()).hexdigest()

# Load user sessions from file
user_sessions = load_user_sessions()

# Main Script
cookie = 'PHPSESSID=fdu8fugv6qa3qag1ik8t7k5pdh; useragent=TW96aWxsYS81LjAgKExpbnV4OyBBbmRyb2lkIDEwOyBLKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTI0LjAuMC4wIE1vYmlsZSBTYWZhcmkvNTM3LjM2; _uafec=Mozilla%2F5.0%20(Linux%3B%20Android%2010%3B%20K)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F124.0.0.0%20Mobile%20Safari%2F537.36;'

# Generate a hash of the cookie
cookie_hash = hash_cookie(cookie)

# Check if user already accessed the service
if cookie_hash in user_sessions:
    print("Bạn chỉ được truy cập dịch vụ một lần!")
    exit()

status, cookie, content = check_login(cookie)
if not status:
    print("Cookie không hợp lệ hoặc chưa đăng nhập trên website !")
    exit()

username, amount = get_info(content)
print("Tool Buff Like Miễn Phí")
print("")

id_post = input("Nhập ID bài viết: ")
if not isnumeric(id_post):
    print("Vui lòng nhập ID bài viết hợp lệ!")
    exit()

server = input(get_server(cookie) + "\nNhập server: ")
if not isnumeric(server) or int(server) > 4:
    print("Vui lòng chọn server hợp lệ!")
    exit()

amount = input("Số lượng: ")
if not isnumeric(amount) or int(amount) > 100:
    print("Vui lòng nhập số lượng hợp lệ (tối đa 100)!")
    exit()

response = buy_like(cookie, id_post, server, amount)
response = get_response(response)
print(response)

# Mark the user session as accessed
save_user_session(cookie_hash)

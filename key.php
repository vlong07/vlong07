import requests
import hashlib
from datetime import datetime

def shorten_url():
    useragent = "Mozilla/5.0 (Linux; Android 10; Active 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"
    
    # Tạo mã băm từ ngày và địa chỉ IP
    txt = hashlib.md5((datetime.now().strftime('%dm%Y') + "toolvip" + requests.get('https://api.ipify.org').text).encode()).hexdigest()[:9]
    
    # URL chứa mã băm
    linkkey = "https://rutgonvlong.000webhostapp.com/key.html?key=" + txt
    
    # Gửi yêu cầu đến dịch vụ rút gọn URL
    response = requests.get("https://web1s.com/api", params={"token": "fdd3048e-2124-4820-90d1-208a2b26ea0d", "url": linkkey})
    
    # Kiểm tra xem yêu cầu đã thành công hay không
    if response.status_code == 200:
        data = response.json()
        return {"success": 200, "link": data["shortenedUrl"], "ip": requests.get('https://api.ipify.org').text}
    else:
        return {"link": "Hãy Dùng Key Phí", "ip": requests.get('https://api.ipify.org').text}

if __name__ == "__main__":
    print(shorten_url())

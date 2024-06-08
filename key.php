from flask import Flask, request, jsonify
import hashlib
import requests

app = Flask(__name__)

@app.route('/shorten_url', methods=['GET'])
def shorten_url():
    useragent = "Mozilla/5.0 (Linux; Android 10; Active 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Mobile Safari/537.36"

    # Tạo mã băm từ ngày và địa chỉ IP
    txt = hashlib.md5((datetime.now().strftime('%dm%Y') + "toolvip" + request.remote_addr).encode()).hexdigest()[:9]
    linkkey = "https://rutgonvlong.000webhostapp.com/key.html?key=" + txt

    # Gửi yêu cầu đến dịch vụ rút gọn URL
    response = requests.get("https://web1s.com/api?token=fdd3048e-2124-4820-90d1-208a2b26ea0d&url=" + linkkey)

    if response.status_code == 200 and linkkey != '':
        data = response.json()
        return jsonify({
            "success": 200,
            #"key": txt,
            "link": data["shortenedUrl"],
            "ip": request.remote_addr
        })
    else:
        return jsonify({
            "link": 'Hãy Dùng Key Phí',
            "ip": request.remote_addr
        })

if __name__ == '__main__':
    app.run(debug=True)

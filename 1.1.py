from flask import Flask, request, jsonify
import hashlib
import datetime

app = Flask(__name__)

@app.route('/toolvip', methods=['GET'])
def toolvip():
    # Get client IP address
    client_ip = request.remote_addr

    # Generate key
    current_date = datetime.datetime.now().strftime('%d%m%Y')
    txt = hashlib.md5((current_date + "toolvip" + client_ip).encode()).hexdigest()[:8]

    # Prepare JSON-like output
    output = {
        "success": "200",
        "key": txt,
        "link": "https://link4m.com/64zIz",
        "ip": client_ip
    }

    # Print JSON-like output to the console or terminal
    print(output)

    # Return a simple message to the client
    return "Key generated"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
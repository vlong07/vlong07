import requests, os, time
from bs4 import BeautifulSoup

os.system("cls" if os.name == "nt" else "clear")
cookie = 'PHPSESSID=a7blhol76l4pmtrgcug99tje9k'
count = 0
while True:
    headers = {
        'authority': 'dvmxh.azdigi.blog',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Cookie': cookie,
        'Origin': 'https://dvmxh.azdigi.blog',
        'Sec-Ch-Ua': '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36'
    }
    data = {
        'draw': 'Rút Thăm',
    }
    rut = requests.post('https://dvmxh.azdigi.blog/game.php', headers=headers, data=data).text
    getdulieu = BeautifulSoup(rut, 'html.parser')
    response = getdulieu.find('div', class_='result')
    info = response.find_all('p')
    rutthuong = info[0].get_text(strip=True)
    luotrut = info[1].get_text(strip=True)
    print(f'{rutthuong} | {luotrut}')
    count += 1
    if count == 10:
        datas = {
            'buy_draws': 'Mua 1 lượt với 1k2 xu'
        }
        mua = requests.post('https://dvmxh.azdigi.blog/game.php', headers=headers, data=datas).text
        getdulieu = BeautifulSoup(mua, 'html.parser')
        response = getdulieu.find('div', class_='result')
        info = response.find_all('p')
        msg = info[0].get_text(strip=True)
        print(msg)
        count = 0
    time.sleep(5)
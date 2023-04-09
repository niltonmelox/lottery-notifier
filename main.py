
__author__ = 'KhiemDH'
__github__ = 'https://github.com/khiemdoan'
__email__ = 'doankhiem.crazy@gmail.com'

import os
from datetime import datetime

import httpx


def send_to_telegram(message):
    bot_token = os.getenv('BOT_TOKEN')
    chat_id = os.getenv('CHAT_ID')
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = httpx.get(url)
    print(response.text)


if __name__ == '__main__':
    url = 'https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/main/results/xsmb_1_year.csv'
    response = httpx.get(url)
    raw = response.text
    rows = [r for r in raw.split('\n') if len(r) > 0]

    last = rows[-1]
    info = [r for r in last.split(',')]
    date = datetime.strptime(info[0], '%Y-%m-%d').date()
    result = info[1:]

    numbers = [int(r) % 100 for r in result]
    special = numbers[0]

    loto_result = []
    for i in range(10):
        category = sorted([d for d in numbers if d // 10 == i])
        category = [f'{d%10:1d}' for d in category]
        category = ', '.join(category) if len(category) > 0 else '-'
        loto_result.append(category)

    rows = [f'{i} | {row}' for i, row in enumerate(loto_result)]

    rows.insert(0, f'Giải đặc biệt: {special:02d}')
    rows.insert(0, f'Kết quả ngày: {date:%d-%m-%Y}')
    rows.insert(1, '')
    rows.insert(3, '')
    message = '\n'.join(rows)

    send_to_telegram(message)

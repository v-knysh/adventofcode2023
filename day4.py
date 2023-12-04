from collections import defaultdict
from dataclasses import dataclass
from typing import List
import requests
import re

input = requests.get('https://adventofcode.com/2023/day/4/input', headers={
    "Host": "adventofcode.com",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://adventofcode.com/2023/day/1",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.902336780.1701458382; _gid=GA1.2.1873937655.1701458382; _ga_MHSNPJKWC7=GS1.2.1701458382.1.1.1701458415.0.0.0; session=53616c7465645f5f79cf7e47167cd40ac0f9294e51facc005594d79acaf9984c818112222621ed0b656b0411a91c3a362fc52198e33ae5c2349cffc10d0100fe",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
})

data = input.content.decode('utf-8').split('\n')
data = [r for r in data if r]

res = 0


card_regex = re.compile(r'Card\s*?(?P<card_id>\d*):(?P<winning_nums>.*)\|(?P<received_nums>.*)')
for j, row in enumerate(data):
    m = card_regex.match(row)
    card_id = m['card_id']
    winning_nums = [int(n) for n in m['winning_nums'].split(' ') if n.isdigit()]
    received_nums = [int(n) for n in m['received_nums'].split(' ') if n.isdigit()]
    card_winning_nums = set(winning_nums).intersection(set(received_nums))
    if card_winning_nums:
        res += 2**(len(card_winning_nums)-1)
    
print(res)
    
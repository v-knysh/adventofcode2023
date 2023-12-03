from collections import defaultdict
from dataclasses import dataclass
from typing import List
import requests
import re

input = requests.get('https://adventofcode.com/2023/day/3/input', headers={
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

blank = '.'

data = input.content.decode('utf-8').split('\n')
data = [r for r in data if r]
# data = data[:20]
res = 0

potential_gears = defaultdict(list)

for j, row in enumerate(data):
    # row = row[:10]
    i = 0
    numbers = []
    numbers_to_add = []
    while i < len(row):
        number_is_part_number = False
        value = row[i]
        if not value.isdigit():
            i += 1
            continue
        m = re.match('(?P<num>\d*).*', row[i:])
        num_str = m['num']
        numbers.append(num_str)
        
        potential_gear_coords = []
        potential_gear_coords.append((j, i-1))
        potential_gear_coords.append((j, i+len(num_str)))
        for k in range(i-1, i+len(num_str)+1):
            potential_gear_coords.append((j-1, k))
            potential_gear_coords.append((j+1, k))       
        
        potential_gear_coords = [
            c for c in potential_gear_coords if all([
                0 <= c[0] < len(data),
                0 <= c[1] < len(row),
            ])
        ]

        0==0
        
        for part_j, part_i in potential_gear_coords:
            if data[part_j][part_i] == '*':
                potential_gears[(part_j, part_i)].append(int(num_str))
            
        
                
                
         
        
        i+=len(num_str)
    print(j, row, numbers)

for coords, values in potential_gears.items():
    if len(values) == 2:
        res += values[0] * values[1]
        print(values[0], values[1], values[0] * values[1]) 
print(res)
    
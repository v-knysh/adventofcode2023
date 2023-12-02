import requests

input = requests.get('https://adventofcode.com/2023/day/1/input', headers={
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
import re

digits_values_dict = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9, 
}


res = 0
for i, row in enumerate(data):
    if not row:
        continue
  
    regex_forward = re.compile(r'\D*?(?P<d1>\d|one|two|three|four|five|six|seven|eight|nine|zero).*')
    regex_reversed = re.compile(r'\D*?(?P<d1>\d|orez|enin|thgie|neves|xis|evif|ruof|eerht|owt|eno).*')    
    
    
    m1 = regex_forward.match(row)['d1']
    d1 = int(digits_values_dict.get(m1, m1))
    m2 = regex_reversed.match(row[::-1])['d1'][::-1]
    d2 = int(digits_values_dict.get(m2, m2))
    num = d1*10 + d2 
    print(row, num)
    res+=num

print(res)    
('ok')
import bisect
from collections import defaultdict
from dataclasses import dataclass, field
import math
import time
from typing import Dict, List
import requests
import re
import numpy as np



if __name__ == "__main__":

    input = requests.get('https://adventofcode.com/2023/day/9/input', headers={
        "Host": "adventofcode.com",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://adventofcode.com/2023/day/9",
        "Connection": "keep-alive",
        "Cookie": "_ga=GA1.2.902336780.1701458382; _gid=GA1.2.1873937655.1701458382; _ga_MHSNPJKWC7=GS1.2.1701458382.1.1.1701458415.0.0.0; session=53616c7465645f5f79cf7e47167cd40ac0f9294e51facc005594d79acaf9984c818112222621ed0b656b0411a91c3a362fc52198e33ae5c2349cffc10d0100fe",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "TE": "trailers"
    })

    data = input.content.decode('utf-8').split('\n')
    # data = ["10  13  16  21  30  45", "0   3   6   9  12  15", '1   3   6  10  15  21']
    res = 0
    for row in data: 
        if not row:
            continue
        nums = [int(i) for i in row.split(' ') if i]
        nums.append(0)
        mx = np.zeros((len(nums), len(nums)))
        mx[0] = np.array(nums)
        
        for i in range(1, len(nums)):
            mx[i,:-i-1] = mx[i-1][1:-i] - mx[i-1,:-i-1]
            if np.all(mx[i]==0):
                break
        
        mx[-1, 0] = 0
        # print(mx)
        if mx[-2, 0] != 0:
            print('test')
        
        for i in range(0, len(nums)-1)[::-1]:
            r = i
            c = len(nums)-1-i
            mx[r, c] = mx[r+1,c-1]+mx[r, c-1]

        # print(mx)
        res += mx[0, -1]
    print(res)
        
        
 
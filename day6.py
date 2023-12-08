import bisect
from collections import defaultdict
from dataclasses import dataclass
import math
from typing import List
import requests
import re

@dataclass
class Race:
    time: int
    distance: int
    
    @property
    def min_int_time(self):
        t = self.time
        d = self.distance
        return math.ceil((t - math.sqrt(t**2 - 4*d)) / 2)
    
    @property
    def max_int_time(self):
        t = self.time
        d = self.distance
        return math.floor((t + math.sqrt(t**2 - 4*d)) / 2)
    
    @property
    def possible_solutions(self):
        res = self.max_int_time - self.min_int_time+1
        return res
        
        # a = self.min_int_time
        # b = self.max_int_time
        # res = (a+b)*(b-a+1)/2 
    

if __name__ == "__main__":

    input = requests.get('https://adventofcode.com/2023/day/6/input', headers={
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

    data = input.content.decode('utf-8')
    input_regex = re.compile('Time:\s*?(?P<time>[\d\s]*)\nDistance:\s*?(?P<Distance>[\d\s]*)')
    input_match = input_regex.match(data)
    
    # races = [Race(i[0], i[1]) for i in zip(
    #     [int(t) for t in input_match['time'].replace(' ', '') if t],
    #     [int(d) for d in input_match['Distance'].replace(' ', '') if d],        
    # )]
    # races[0].max_int_time
    
    races = [Race(
        int(input_match['time'].replace(' ', '')),
        int(input_match['Distance'].replace(' ', ''))
    )]
    r = 1
    for i in races:
        r *= i.possible_solutions
    print(r)
    
    
    
    

import bisect
from collections import defaultdict
from dataclasses import dataclass
import math
from typing import List
import requests
import re
from collections import Counter



@dataclass
class Hand:
    cards: str
    bid: int
    
    reg = re.compile('(?P<hand>[\d|A|K|Q|J|T]{5})\s(?P<bid>\d+)')
    @classmethod
    def from_str(cls, str):
        m = cls.reg.match(str)
        return cls(m['hand'], int(m['bid']))
    
    @property
    def htype(self):
        cards = self.cards
        if cards == "JJJJJ":
            return 7
        if "J" in cards:
            counter = Counter(self.cards.replace('J', ''))
            most_common = counter.most_common(1)
            cards = cards.replace("J", most_common[0][0])
        
        
        counts = list(Counter(cards).values())
                 
        
        if 5 in counts:
            rank = 7
        elif 4 in counts:
            rank = 6
        elif 3 in counts and 2 in counts:
            rank = 5
        elif 3 in counts and 2 not in counts:
            rank = 4
        elif counts.count(2) == 2:
            rank = 3
        elif counts.count(2) == 1:
            rank = 2
        else:
            rank = 1
        return rank
    
    @property
    def hand_values(self):
        orig = 'AKQT98765432J'
        values = 'CBA9876543210'
        m={k:v for k,v in zip(orig, values)}
        return ''.join([m[s] for s in self.cards])
           
    @property                   
    def sort_key(self) -> str:
        return f"{self.htype} {self.hand_values}"

if __name__ == "__main__":

    input = requests.get('https://adventofcode.com/2023/day/7/input', headers={
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

    hands = []
    data = input.content.decode('utf-8').split('\n')
    for i, row in enumerate([d for d in data if d]):
        h = Hand.from_str(row)
        bisect.insort(hands, h, key=lambda h: h.sort_key)
    
    res = 0
    for i, hand in enumerate(hands):
        res += (i+1)*hand.bid
    print(res)    
    



    
    
    
    

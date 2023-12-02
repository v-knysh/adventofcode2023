from dataclasses import dataclass
from typing import List
import requests
import re

input = requests.get('https://adventofcode.com/2023/day/2/input', headers={
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

max_cubes = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


@dataclass
class GameSet:
    red: int = 0
    green: int = 0
    blue: int = 0

    def __add__(self, other):
        return GameSet(
            red = self.red + other.red,
            green = self.green + other.green,
            blue = self.blue + other.blue,
        )
    
    def __mul__(self, other):
        return GameSet(
            red = max(self.red, other.red),
            green = max(self.green, other.green),
            blue = max(self.blue, other.blue),
        )
    
    def __abs__(self):
        return self.red*self.blue*self.green


@dataclass
class Game:
    id: int
    sets: List[GameSet] 

base_game = GameSet(**max_cubes)
def is_game_valid(game):
    return all([
        game.red<=base_game.red,
        game.green<=base_game.green,
        game.blue<=base_game.blue,
    ])
    

res = 0
    
for i, row in enumerate(filter(bool, data)):
    game_valid = True
    m = re.match(r'Game (?P<game_id>\d*): (?P<sets>.*)', row)
    game_id = m['game_id']
    min_req_gameset = GameSet()
    gamesets = []
    for gameset_str in m['sets'].split(';'):
        gameset = {}
        for color_num_str in gameset_str.split(','):
            m = re.match(r'\s*((?P<num1>\d*)\s(?P<color1>\w*))\s*', color_num_str)
            gameset[m['color1']] = int(m['num1'])
        gameset = GameSet(**gameset)
        if not is_game_valid(gameset):
            game_valid = False
        gamesets.append(gameset)
        min_req_gameset *= gameset
    
        
    res += abs(min_req_gameset)
        
    

print(res)
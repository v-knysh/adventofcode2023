import bisect
from collections import defaultdict
from dataclasses import dataclass
from typing import List
import requests
import re

input = requests.get('https://adventofcode.com/2023/day/5/input', headers={
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
# data = [r for r in data if r]

input_regex = re.compile(r"""seeds: (?P<seeds>[\d|\s]*)\nseed-to-soil map:\n(?P<seed_to_soil>[\d\s]*)\n\nsoil-to-fertilizer map:\n(?P<soil_to_fertilizer>[\d\s]*)\n\nfertilizer-to-water map:\n(?P<fertilizer_to_water>[\d\s]*)\n\nwater-to-light map:\n(?P<water_to_light>[\d\s]*)\n\nlight-to-temperature map:\n(?P<light_to_temperature>[\d\s]*)\n\ntemperature-to-humidity map:\n(?P<temperature_to_humidity>[\d\s]*)\n\nhumidity-to-location map:\n(?P<humidity_to_location>[\d\s]*)\n""")

data_match = input_regex.match(data)



class Range():
    def __init__(self, dest, source, step) -> None:
        self.dest_start = int(dest)
        self.dest_end = int(dest) + int(step)
        self.source_start = int(source)
        self.source_end = int(source) + int(step)
    
    def dest_value(self, source_value):
        if self.source_start <= source_value <= self.source_end:
            return self.dest_start + (source_value - self.source_start)
        else:
            return source_value
    
    @classmethod
    def from_str(cls, row):
        row_regex = re.compile(r'(?P<dest>\d+)\s(?P<source>\d+)\s(?P<step>\d+)')
        m = row_regex.match(row)
        return cls(m['dest'], m['source'], m['step'])
        

def map_function_factory(map_str):
    ranges = []
    for row in map_str.split('\n'):
        r = Range.from_str(row)
        bisect.insort(ranges, r, key=lambda r: r.source_start)
    
    def map_function(value):
        r = [r for r in ranges if r.source_start <= value <= r.source_end]
        if r:
            result = r[0].dest_value(value)
        else:
            result = value
        return result
    return map_function

seed_to_soil = map_function_factory(data_match['seed_to_soil'])
soil_to_fertilizer = map_function_factory(data_match['soil_to_fertilizer'])
fertilizer_to_water = map_function_factory(data_match['fertilizer_to_water'])
water_to_light = map_function_factory(data_match['water_to_light'])
light_to_temperature = map_function_factory(data_match['light_to_temperature'])
temperature_to_humidity = map_function_factory(data_match['temperature_to_humidity'])
humidity_to_location = map_function_factory(data_match['humidity_to_location'])

seeds_data = {}
min_location = {}

seeds = data_match['seeds'].split(' ')
# seed_ranges = [int(s) for s in data_match['seeds'].split(' ')]
# for i in range(0, len(seed_ranges), 2):
#     seeds.extend(list(range(seed_ranges[i], seed_ranges[i+1])))
    
print(len(seeds))



percent_step = len(seeds) // 100
min_location = float('inf')
for i, s in enumerate(seeds):
    if i % percent_step == 0:
        progress_percent = (i // percent_step) + 1
        print(f"Processed {progress_percent}%")
    seed = int(s)
    soil = seed_to_soil(int(seed))
    fertilizer = soil_to_fertilizer(soil)
    water = fertilizer_to_water(fertilizer)
    light = water_to_light(water)
    temperature = light_to_temperature(light)
    humidity = temperature_to_humidity(temperature)
    location = humidity_to_location(humidity)
    
    min_location = min(min_location, location)
    # seeds_data[seed] = {
    #     'seed': seed,
    #     'soil': soil,
    #     'fertilizer': fertilizer,
    #     'water': water,
    #     'light': light,
    #     'temperature': temperature,
    #     'humidity': humidity,
    #     'location': location,
    # }



print('ok')
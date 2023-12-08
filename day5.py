import bisect
from collections import defaultdict
from dataclasses import dataclass
from typing import List
import requests
import re

input_regex = re.compile(r"""seeds: (?P<seeds>[\d|\s]*)\nseed-to-soil map:\n(?P<seed_to_soil>[\d\s]*)\n\nsoil-to-fertilizer map:\n(?P<soil_to_fertilizer>[\d\s]*)\n\nfertilizer-to-water map:\n(?P<fertilizer_to_water>[\d\s]*)\n\nwater-to-light map:\n(?P<water_to_light>[\d\s]*)\n\nlight-to-temperature map:\n(?P<light_to_temperature>[\d\s]*)\n\ntemperature-to-humidity map:\n(?P<temperature_to_humidity>[\d\s]*)\n\nhumidity-to-location map:\n(?P<humidity_to_location>[\d\s]*)\n""")


@dataclass
class Range():
    start: int
    end: int  

class RangeMap():
    def __init__(self, dest_start, dest_end, source_start, source_end) -> None:
        self.dest_start = dest_start
        self.dest_end = dest_end
        self.source_start = source_start
        self.source_end = source_end
    
    @property
    def step(self):
        return self.source_end - self.source_start
    
    def dest_value(self, source_value):
        if self.source_start <= source_value <= self.source_end:
            return self.dest_start + (source_value - self.source_start)
        else:
            return source_value
    
    def split_values_range(self, values_range):
        res = {
            'preix': None,
            'ix': None,
            'postix': None,
        }
        
        end_preintersection = min(self.source_start-1, values_range.end)
        start_preintersection = values_range.start
        if start_preintersection < end_preintersection:
            res['preix'] = Range(start_preintersection, end_preintersection)
        
        start_intersection = max(self.source_start, values_range.start)
        end_intersection = min(self.source_end, values_range.end)
        if start_intersection < end_intersection:
            res['ix'] = Range(start_intersection, end_intersection)
        
        start_postintersection = max(self.source_end+1, values_range.start)
        end_postintersection = values_range.end
        if start_postintersection < end_postintersection:
            res['postix'] = Range(start_postintersection, end_postintersection)
        
        return res


    def map_values_range(self, range:Range):
        # range completely inside range
        if self.source_start <= range.start and range.end <= self.source_end:
            shift = self.dest_start - self.source_start
            return Range(range.start+shift, range.end+shift)
        raise ValueError
    
           
           
    @classmethod
    def from_str(cls, row):
        row_regex = re.compile(r'(?P<dest>\d+)\s(?P<source>\d+)\s(?P<step>\d+)')
        m = row_regex.match(row)
        return cls(
            int(m['dest']),
            int(m['dest']) + int(m['step'])-1,
            int(m['source']),
            int(m['source']) + int(m['step'])-1
        )
    
    def intersects(self, range):
        return self.source_start <= range.end and range.start <= self.source_end

    def contains(self, range):
        return self.source_start <= range.start and range.end <= self.source_end

      
      
class MapFunction:
    def __init__(self, ranges) -> None:
        self.ranges = ranges
    
    @classmethod
    def from_map_str(cls, map_str):
        ranges = []
        for row in map_str.split('\n'):
            r = RangeMap.from_str(row)
            bisect.insort(ranges, r, key=lambda r: r.source_start)
        return cls(ranges)
   
    def __call__(self, value):
        if isinstance(value, int):
            return self._call_int(value)
        else:
            return self._call_range(value)
        
    def _call_int(self, value):
        r = [r for r in self.ranges if r.source_start <= value <= r.source_end]
        if r:
            result = r[0].dest_value(value)
        else:
            result = value
        return result

    def _call_range(self, ranges):
        splitted_ranges = self._splitted_ranges(ranges)
        res = []
        for range in splitted_ranges:
            for mrange in self.ranges:
                if mrange.contains(range):
                    res.append(mrange.map_values_range(range))
                    break
            else:
                res.append(range)
        return res
        
    def _splitted_ranges(self, ranges):
        ranges.sort(key=lambda x:x.start)
        splitted_ranges = []
        wip_ranges = [r for r in ranges]
        
        while wip_ranges:
            range = wip_ranges.pop(0)
            intersectible_source_ranges = [sr for sr in self.ranges if sr.intersects(range)]
            if not intersectible_source_ranges:
                splitted_ranges.append(range)
                continue
            sr = intersectible_source_ranges[0]
            spl = sr.split_values_range(range)

            if spl['preix']:
                splitted_ranges.append(spl['preix'])
            if spl['ix']:
                splitted_ranges.append(spl['ix'])
            if spl['postix']:
                if spl['postix'] == range:
                    splitted_ranges.append(spl['postix'])
                else:
                    wip_ranges.insert(0, spl['postix'])
                    
        print('ok')
        return splitted_ranges
                
                    
                
             
        

if __name__ == "__main__":

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

    data_match = input_regex.match(data)


    seed_to_soil = MapFunction.from_map_str(data_match['seed_to_soil'])
    soil_to_fertilizer = MapFunction.from_map_str(data_match['soil_to_fertilizer'])
    fertilizer_to_water = MapFunction.from_map_str(data_match['fertilizer_to_water'])
    water_to_light = MapFunction.from_map_str(data_match['water_to_light'])
    light_to_temperature = MapFunction.from_map_str(data_match['light_to_temperature'])
    temperature_to_humidity = MapFunction.from_map_str(data_match['temperature_to_humidity'])
    humidity_to_location = MapFunction.from_map_str(data_match['humidity_to_location'])



    seed_ranges = []
    seeds_input = [int(s) for s in data_match['seeds'].split(' ')]
    for i in range(0, len(seeds_input), 2):
        seed_ranges.append(Range(seeds_input[i], seeds_input[i]+seeds_input[i+1]-1))
        
    print(len(seed_ranges))

    soil_ranges = seed_to_soil(seed_ranges)
    fertilizer_ranges = soil_to_fertilizer(soil_ranges)
    water_ranges = fertilizer_to_water(fertilizer_ranges)
    light_ranges = water_to_light(water_ranges)
    temperature_ranges = light_to_temperature(light_ranges)
    humidity_ranges = temperature_to_humidity(temperature_ranges)
    location_ranges = humidity_to_location(humidity_ranges)
        

    print('ok')
import bisect
from collections import defaultdict
from dataclasses import dataclass, field
import math
import time
from typing import Dict, List
import requests
import re

START_NODE = 'AAA'
FINAL_NODE = 'ZZZ'


@dataclass
class Node:
    name: str
    left:str
    right:str
    calls: Dict[str, 'ExecutionResult'] = field(default_factory=dict)
    
    r = re.compile(r'(?P<name>\w{3}) = \((?P<left>\w{3}), (?P<right>\w{3})\)')
    @classmethod
    def from_str(cls, s):
        m = cls.r.match(s)
        return cls(
            name=m['name'],
            left=m['left'],
            right=m['right'],
        )
    
    def execute(self, command:str) -> 'ExecutionResult':
        if command in self.calls:
            return self.calls[command]

        # print(f'calling {self.name} - {command}')
        if len(command) == 1:
            if command == 'L':
                node_id = self.left
            if command == 'R':
                node_id = self.right
            
            ex_com_res = ExecutionResult(
                node=nodes[node_id],
                steps=1,
            )
        else:
            ex_res1 = self.execute(command[:-1])
            if ex_res1.completed:
                ex_com_res = ex_res1
            else:
                ex_res2 = ex_res1.node.execute(command[-1])
                ex_com_res = ExecutionResult(
                    node=ex_res2.node,
                    steps=ex_res1.steps+1
                ) 
        self.calls[command] = ex_com_res
        return ex_com_res

nodes: Dict[str, Node] = {}
        

@dataclass
class ExecutionResult:
    node: Node
    steps: int
    
    @property
    def completed(self):
        return self.node.name == FINAL_NODE 
    

if __name__ == "__main__":

    input = requests.get('https://adventofcode.com/2023/day/8/input', headers={
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
    command = data[0]
    
    for row in data[1:]:
        if not row:
            continue
        node = Node.from_str(row)
        nodes[node.name] = node
    print('ok')
    
    start = time.time()
    for n in list(nodes.values()):
        n.execute(command*3)
    end = time.time()
    
    print("Precalculations took {:.6f} seconds to execute.".format(end-start))
    
    start_time = time.time()
    print("Calculations started at:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    # execution_result = nodes[START_NODE].execute(command[:5])
    execution_result = nodes[START_NODE].execute(command*3)
    steps = execution_result.steps
    while execution_result.completed != True:
        execution_result = execution_result.node.execute(command)
        steps += execution_result.steps
        print(steps)
    print(steps)
    
    end = time.time()
    print("Calculations took {:.6f} seconds to execute.".format(end-start_time))
    print('ok')
        
    
    
    

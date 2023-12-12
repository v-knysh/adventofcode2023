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
LEN_COMMAND = 307
COMMAND = "LRLRRRLRRLRRRLRRRLLLLLRRRLRLRRLRLRLRRLRRLRRRLRLRLRRLLRLRRLRRLRRLRRRLLRRRLRRRLRRLRLLLRRLRRRLRLRRLRRRLRRLRLLLRRRLRRLRRLRRRLRRRLRRRLRLRLRLRRRLRRRLLLRRLLRRRLRLRLRRRLRRRLRRLRRRLRLRLLRRRLRLRRLRLRLRRLLLRRRLRRRLRRLRRLRLRRLLRRLRRRLRRRLLRRRLRRLRLLRRLRLRRLLRRRLLLLRRLRRRLRLRRLLRLLRRRLLRRLLRRRLRRRLRRLLRLRLLRRLLRLLLRRRR"
# COMMAND = "LR"


@dataclass
class Node:
    name: str
    left:str
    right:str
    calls: Dict[str, 'ExecutionResult'] = field(default_factory=dict)
    
    r = re.compile(r'(?P<name>.{3}) = \((?P<left>.{3}), (?P<right>.{3})\)')
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
        if not command:
            print(command)
            raise Exception
        # print(f'calling {self.name} - {command}')

        
        if command.isdigit():
            c = int(command)
            if c==1:
                return self.execute(COMMAND)
            ex_res1 = self.execute(str(int(c/2)))
            if ex_res1.completed:
                ex_com_res = ex_res1
            else:
                ex_res2 = ex_res1.node.execute(str(int(c-c/2)))
                ex_com_res = ExecutionResult(
                    node=ex_res2.node,
                    steps=ex_res1.steps+ex_res2.steps
                )
        else:
            if len(command) > len(COMMAND):
                l = len(command)
                quotient = l / LEN_COMMAND
                remainder = l % LEN_COMMAND
                ex_res1 = self.execute(str(int(quotient)))
                if ex_res1.completed:
                    ex_com_res = ex_res1
                elif remainder:
                    c = command[len(command)-remainder:]
                    if not c:
                        raise Exception
                    ex_res2 = ex_res1.node.execute(command[-remainder:])
                    ex_com_res = ExecutionResult(
                        node=ex_res2.node,
                        steps=ex_res1.steps+ex_res2.steps
                    ) 
                else:
                    ex_com_res = ex_res1


            elif len(command) == 1:
                if command == 'L':
                    node_id = self.left
                elif command == 'R':
                    node_id = self.right
                else:
                    raise Exception(command)
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
        return self.node.name[-1] == 'Z'
    
    def __add__(self, other):
        if self.node != other.node:
            raise ValueError
        return ExecutionResult(self.node, self.steps+other.steps)
      

@dataclass
class NodeExecutor():
    node: Node
    steps: int = 0
    command: str = COMMAND
    last_completed_execution_result: ExecutionResult = None
    
    def next(self):
        if self.last_completed_execution_result:
            remaining_part_command = self.command[self.steps % LEN_COMMAND:] or self.command
            node = self.last_completed_execution_result.node
        else:
            node = self.node
            remaining_part_command = self.command
        
        execution_result = node.execute(remaining_part_command)
        self.steps += execution_result.steps
        # i = int(self.steps/LEN_COMMAND+1)
        while execution_result.completed != True:
            # i*=2
            execution_result = execution_result.node.execute('128')
            self.steps += execution_result.steps
        self.last_completed_execution_result = execution_result
        return execution_result    


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
#     data = """LR

# 11A = (11B, XXX)
# 11B = (XXX, 11Z)
# 11Z = (11B, XXX)
# 22A = (22B, XXX)
# 22B = (22C, 22C)
# 22C = (22Z, 22Z)
# 22Z = (22B, 22B)
# XXX = (XXX, XXX)
# """.split('\n')
    
    
    
    command = data[0]
    
    for row in data[1:]:
        if not row:
            continue
        node = Node.from_str(row)
        nodes[node.name] = node
    print('ok')
    
    start = time.time()
    for n in list(nodes.values()):
        n.execute('2047')
        n.execute('2097152')
        
    end = time.time()
    
    print("Precalculations took {:.6f} seconds to execute.".format(end-start))
    
    start_time = time.time()
    print("Calculations started at:", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(start_time)))
    
    target_value = 0
    a_node_executors = [NodeExecutor(n) for n in nodes.values() if n.name[-1]=='A']
    # a_node_executors = [NodeExecutor(n) for n in nodes.values() if n.name=='22A']

    
    for ne in a_node_executors:
        r = ne.next()
        print(ne.node.name, ne.steps, r.node.name)
        
        ne2 = NodeExecutor(r.node)
        r2 = ne2.next()
        print(ne2.node.name, ne2.steps, r2.node.name)
        while not ne2.node.name == r2.node.name:
            r2 = ne2.next()
            print(ne2.node.name, ne2.steps, r2.node.name)
        print('next')
        
    # while not all(ne.steps == a_node_executors[0].steps for ne in a_node_executors):
    #     min_ne = min(a_node_executors, key=lambda x: x.steps)
    #     print(min_ne.node.name, '{:,}'.format(min_ne.steps))
    #     min_ne.next()
    # print(a_node_executors[0].steps)
    
    end = time.time()
    print("Calculations took {:.6f} seconds to execute.".format(end-start_time))
    print('ok')
        
    
    
    

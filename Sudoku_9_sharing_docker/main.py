from utils import squares, print_grid
from utils import timer, parse_puzzle
from utils import is_solved, place, valid_grid
from utils import  min_possible_values

import os
import json
import argparse
import asyncio
import psutil
from threading import Lock
from time import time
from aio_pika import connect_robust, Message
from functools import partial


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num-threads", type = int, default = 2, help = "# of threads run parallel")
    return vars(ap.parse_args())
def load_puzzles():
    with open("config.json", 'r') as f:
        data = json.loads(f.read())
    return data['puzzles']


class Sudoku:
    EXCHANGE = 'exchange'
    QUEUE_NAME = "fringe"
    lock = Lock()
    print = staticmethod(print_grid)
    def __init__(self):
        self.waiting = 0
        self.fringe = []
        self.explored = []
        self.channel = None
        self.connection = None
        self.exchange = None
        self.queue = None


    async def solve(self, num_threads):
    
        # while self.waiting < num_threads:
            # while not self.fringe:
            #     self.waiting += 1
            #     with Sudoku.cv:
            #         Sudoku.cv.wait()
            #     self.waiting -= 1
        while True:
            await self.queue.consume(self.consume)
            # stack
            if not self.fringe:
                continue
            with Sudoku.lock:
                grid = self.fringe.pop()
            if grid in self.explored:
                continue
            if is_solved(grid):
                await self.exchange.publish(Message(json.dumps(grid).encode('utf-8')), routing_key = Sudoku.QUEUE_NAME)
                return grid
            self.explored.append(grid)
            _, square = min_possible_values(grid)
            for digit in grid[square]:
                new_grid = place(grid.copy(), square, digit)
                if new_grid and valid_grid(new_grid):
                    await self.exchange.publish(Message(json.dumps(new_grid).encode('utf-8')), routing_key = Sudoku.QUEUE_NAME)
        return False        
    async def on_open_connection(self, loop):
        self.connection = await connect_robust("amqp://guest:guest@rabbitmq-server", loop = loop)
    async def on_open_channel(self):
        self.channel = await self.connection.channel(publisher_confirms = False)
        await self.channel.set_qos(prefetch_count = 1)
        self.exchange = self.channel.default_exchange
        self.queue = await self.channel.declare_queue(Sudoku.QUEUE_NAME)
        # await self.queue.bind(self.exchange)
        await self.queue.consume(self.consume)
    async def connect(self, loop): 
        await self.on_open_connection(loop)
        await self.on_open_channel()
    async def run(self, loop, grid, num_threads):
        await asyncio.sleep(5)
        await self.connect(loop)
        await self.exchange.publish(Message(json.dumps(grid).encode('utf-8')), routing_key = Sudoku.QUEUE_NAME)
 
        start_time = time()
        print(hash(self), start_time)
        result = await self.solve(num_threads)
        elapsed_time = time() - start_time
        print(hash(self), elapsed_time + start_time)
        # await self.channel.close()
        return elapsed_time

    async def consume(self, message):
        with message.process():
            body = message.body.decode('utf-8')
            body = json.loads(body)
            with Sudoku.lock:
                self.fringe.append(body)
   
def main(args):
    num_threads = args['num_threads']
    process = psutil.Process(os.getpid())
    total_times = []
    total_memories = []
    for i in range(1):
        puzzles = load_puzzles()
        grid = parse_puzzle(puzzles[0])
        loop = asyncio.get_event_loop()
        elapsed_time = loop.run_until_complete(Sudoku().run(loop, grid, num_threads))
        total_times.append(elapsed_time)
        total_memories.append(process.memory_info().rss / 1024 ** 2)
    print(f'["INFO"] Average time: {sum(total_times)/ len(total_times): .6f}')
    print(f'["INFO"] Average usage memory: {sum(total_memories)/ len(total_memories): .4f} MB')
if __name__ == "__main__":
    main(parse_args())
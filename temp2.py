import asyncio
from aioconsole import ainput
from time import time

async def monit():
    while True:
        await asyncio.sleep(2)
        print(f'Time {time()}')

async def func():
    await asyncio.sleep(10)

async def inp():
    while True:
        a= await ainput()

async def main():
    task = asyncio.create_task(monit())
    task = asyncio.create_task(inp())
    await func()

result = asyncio.run(main())

import json
import aiofile
import asyncio
import aiopath

q = {'1': 'one', '2': 'two', '3': 'three'}


# async def read_f():
#     async with aiofile.async_open('data.json', 'r') as rf:
#         ww = await rf.read()
#     return ww

async def path_find():
    p = aiopath.AsyncPath('client_log.json')
    print(await p.exists())
    print(await p.is_file())
    return p


async def main():
    # await write_f()
    # data = await read_f()
    p = await path_find()
    print(p)
    
asyncio.run(main())

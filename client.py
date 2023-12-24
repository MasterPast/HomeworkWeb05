import asyncio
import aiopath
import json
import websockets
import aiofile

file_name = 'client_log.json'


async def append_file(data):
    async with aiofile.async_open('client_log.json', 'a') as wf:
        await wf.write(json.dumps(data, indent=2))

async def client_console():

    command = input('Send to server <<< ')
    if command == 'exit':
        exit()

    return command

async def file_is_exist(file_name):

    fn = aiopath.AsyncPath(file_name)
    mark_1 = await fn.exists()
    mark_2 = await fn.is_file()
    
    return mark_1, mark_2

async def form_output(data, date):

    print(f'Date : {date}')
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))

async def main():
    
    open_socket = True
    uri = 'ws://localhost:8765'
    
    while open_socket == True:
        async with websockets.connect(uri, ping_timeout=20) as websocket:
            command = await client_console()
            await websocket.send(command)
            data = await websocket.recv()            
            decode_data = json.loads(data)
            mark_1, mark_2 = await file_is_exist(file_name)
            if mark_1 == True and mark_2 == True:
                await append_file(decode_data)
            else:
                await write_file(decode_data)
            for date, currency_exchange in decode_data.items():
                await form_output(currency_exchange, date)

async def write_file(data):
    async with aiofile.async_open('client_log.json', 'w') as wf:
        await wf.write(json.dumps(data, indent=2))


if __name__ == '__main__':
    asyncio.run(main())
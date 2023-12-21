import aiohttp
import asyncio
import json
import websockets
from datetime import date, datetime
days_ago = 0

async def hello(websocket):
    name = await websocket.recv()
    
    try:
        days_ago = int(name)
    except ValueError:
        pass
    async with aiohttp.ClientSession() as session:
    
        if 10 > days_ago > 0:
            print('Hard request')
            delta_day = date.today().day - days_ago
            response_day = date(year=2023, month=12,
                                day=delta_day).strftime("%d.%m.%Y")        
            response_construct = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + response_day
            print(response_construct)
            async with session.get(response_construct) as response:
                response.body = await response.text()
                decode_data = json.loads(response.body)
                for elems in decode_data['exchangeRate']:
                    if elems['currency'] == 'USD':
                        print(elems)
                    if elems['currency'] == 'EUR':
                        print(elems)
                # print(decode_data)
        else:
            print('Easy request')
            async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
                response.body = await response.text()
                decode_data = json.loads(response.body)
                print(decode_data)


    greeting = f'Hello {name}!!!'
    await websocket.send(greeting)
    print(f'>>> {greeting}')

async def main():
    async with websockets.serve(hello, 'localhost', 8765):
        await asyncio.Future() 

if __name__ == '__main__':
    asyncio.run(main())   
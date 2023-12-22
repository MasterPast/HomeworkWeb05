import asyncio
import json
import websockets


async def hello():
    
    open_socket = True
    uri = 'ws://localhost:8765'
    
    while open_socket == True:
        async with websockets.connect(uri, ping_timeout=20) as websocket:
            
            name = input('Send to server <<< ')
            if name == 'exit':
                await websocket.send('exit')
                break

            await websocket.send(name)

            data = await websocket.recv()
            decode_data = json.loads(data)
            for date, currency_exchange in decode_data.items():
                await pretty_view(currency_exchange, date)

async def pretty_view(data, date):
    print(f'Date : {date}')
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


if __name__ == '__main__':
    asyncio.run(hello())
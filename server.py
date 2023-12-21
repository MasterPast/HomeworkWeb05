import aiohttp
import asyncio
import json
import websockets
from datetime import date, datetime
days_ago = 0


async def data_adapter_date(data: dict):
    return [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]


async def data_adapter_today(data: dict):
    
    data_from_json = json.loads(data)
    res = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data_from_json]
    ret = {date.today().strftime("%d.%m.%Y"): res}
    print(ret)
    return ret


async def hello(websocket):

    name = await websocket.recv()
    
    try:
        days_ago = int(name)
    except ValueError:
        pass
    async with aiohttp.ClientSession() as session:
        currency_exchange = []
        if 10 > days_ago > 0:
            delta_day = date.today().day - days_ago
            response_day = date(year=2023, month=12,
                                day=delta_day).strftime("%d.%m.%Y")        
            response_construct = 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + response_day
            async with session.get(response_construct) as response:
                response.body = await response.text()
                decode_data = json.loads(response.body)
                for elems in decode_data['exchangeRate']:
                    if elems['currency'] == 'USD':
                        currency_exchange.append(elems)
                    if elems['currency'] == 'EUR':
                        currency_exchange.append(elems)
                        print(type(currency_exchange))
                data = await data_adapter_date(currency_exchange)
                # print(type(data))
        else:
            async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
                currency_exchange = await response.text()
                data = await data_adapter_today(currency_exchange)

                                        
    # print(return_data)
                
    return_data = json.dumps(data)
    greeting = f'Hello {name}!!!'
    await websocket.send(return_data)
    print(f'>>> {greeting}')



async def main():
    async with websockets.serve(hello, 'localhost', 8765):
        await asyncio.Future() 

if __name__ == '__main__':
    asyncio.run(main())   
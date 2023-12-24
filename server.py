import aiohttp
import asyncio
import json
import logging
import websockets
from aioconsole import ainput
from currencies import currencies
from datetime import date

days_ago = 0
logging.basicConfig(level=logging.INFO, filename="server.log", filemode="w",
                    format="%(asctime)s %(message)s")


async def data_adapter_date(data_from_json: dict, response_day):    
    
    res = [{f"{el.get('currency')}": {"buy": float(el.get('purchaseRate')), "sale": float(el.get('saleRate'))}} for el in data_from_json]
    ret = {response_day: res}
    return ret

async def data_adapter_today(data_from_json: dict):
    
    res = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data_from_json]
    ret = {date.today().strftime("%d.%m.%Y"): res}
    return ret

async def parse_command(command):
    
    commands = command.split()
    logging.info(commands)
    return commands

async def validate_command(commands):
    
    days_ago = 0
    extra_currency = ''
    if len(commands) > 0:
        if commands[0] == 'exchange':
            if len(commands) > 1:
                if commands[1].isdigit():
                    days_ago = int(commands[1])
                if len(commands) > 2:
                    if commands[2] in currencies:
                        extra_currency = commands[2]
        
    return days_ago, extra_currency

async def choose_currency(response_body, extra_currency):

    currency_exchange = []
    decode_data = json.loads(response_body)
    for elems in decode_data['exchangeRate']:
        if elems['currency'] == 'USD':
            currency_exchange.append(elems)
        if elems['currency'] == 'EUR':
            currency_exchange.append(elems)
        if elems['currency'] == extra_currency:
            elem_modify = elems.copy()
            elem_modify['saleRate'] = elem_modify.pop('saleRateNB')
            elem_modify['purchaseRate'] = elem_modify.pop('purchaseRateNB')
            currency_exchange.append(elem_modify)

    return currency_exchange

def response_day(days_ago):
    
    delta_day = date.today().day - days_ago
    return date(year=2023, month=12, day=delta_day).strftime("%d.%m.%Y")        

async def response_constructor(days_ago):

        if 10 > days_ago > 0:            
            return 'https://api.privatbank.ua/p24api/exchange_rates?json&date=' + response_day(days_ago)
        else:
            return 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

async def open_websocket(websocket):

    command = await websocket.recv()
    logging.info(command)
    commands = await parse_command(command)
    days_ago, extra_currency = await validate_command(commands)
    async with aiohttp.ClientSession() as session:
        response_modified = await response_constructor(days_ago)
        async with session.get(response_modified) as response:
            if 10 > days_ago > 0:
                response.body = await response.text()
                currency_exchange = await choose_currency(response.body, extra_currency)       
                data = await data_adapter_date(currency_exchange, response_day(days_ago))            
            else:
                currency_exchange = await response.text()
                data_from_json = json.loads(currency_exchange)
                data = await data_adapter_today(data_from_json)
    return_data = json.dumps(data)
    logging.info(return_data)
    await websocket.send(return_data)

async def server_down():
    logging.info('Server is stopped.')
    exit()

async def server_console():
    
    while True:
        command = await ainput('server>>> ')
        if command == 'exit':
            await server_down()
    
async def ws():
    async with websockets.serve(open_websocket, 'localhost', 8765):
        await asyncio.Future() 

async def main():
    task = asyncio.create_task(server_console())
    await ws()
    

if __name__ == '__main__':
    asyncio.run(main())   
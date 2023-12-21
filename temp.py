import aiohttp
import asyncio
import json


async def main():
    async with aiohttp.ClientSession(headers={'Date': 'Wed, 20 Dec 2023 12:23:52 GMT'}) as session:
        # async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
        async with session.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=20.12.2023') as response:
        
        # async with session.get('http://httpbin.org/get') as response:

            print(response.status)
            print(response.headers)

            print(response)
            response.body = await response.text()
            # print(response.body)

            # print(response.bank)

            decode_data = json.loads(response.body)
            
            # for elems in decode_data['exchangeRate']:
            #     if elems['currency'] == 'USD':
            #         print(elems)
            #     if elems['currency'] == 'EUR':
            #         print(elems)


            print(decode_data)
            
            # for el in response.body:
            #     print(el)
    return response.body

if __name__ == '__main__':
    data = asyncio.run(main())

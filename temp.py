import aiohttp
import asyncio
import json

date = '12.12.2023'

async def main():
    async with aiohttp.ClientSession(headers={'Date': 'Wed, 20 Dec 2023 12:23:52 GMT'}) as session:
        async with session.get('https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5') as response:
            # async with session.get('https://api.privatbank.ua/p24api/exchange_rates?json&date=20.12.2023') as response:

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

    return decode_data


def data_adapter(data: dict):
    ret = [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]
    print(ret)
    return ret

def pretty_view(data):
    print(f'Date : {date}')
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


if __name__ == '__main__':
    data = asyncio.run(main())
    pretty_view(data_adapter(data))

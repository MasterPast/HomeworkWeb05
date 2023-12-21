from datetime import date, datetime
import asyncio

datar = [{"ccy": "EUR", "base_ccy": "UAH", "buy": "40.90000", "sale": "41.90000"}, {
    "ccy": "USD", "base_ccy": "UAH", "buy": "37.40000", "sale": "37.90000"}]

datan = [{'EUR': {'buy': 40.9, 'sale': 41.9}},
         {'USD': {'buy': 37.4, 'sale': 37.9}}]


async def adder_async(a, b):
    return a+b


def data_adapter(data: dict):
    return [{f"{el.get('ccy')}": {"buy": float(el.get('buy')), "sale": float(el.get('sale'))}} for el in data]


def pretty_view(data):
    pattern = '|{:^10}|{:^10}|{:^10}|'
    print(pattern.format('currency', 'sale', 'buy'))
    for el in data:
        currency, *_ = el.keys()
        buy = el.get(currency).get('buy')
        sale = el.get(currency).get('sale')
        print(pattern.format(currency, sale, buy))


async def main():
    res = await adder_async(3, 8)
    print(res)

print(date.today().strftime("%d.%m.%Y"))
print(type(datar), type(datan))
asyncio.run(main())
# print(adder_async(3, 8))

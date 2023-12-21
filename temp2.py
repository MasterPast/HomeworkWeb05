from datetime import date, datetim

a = {'date': '2233', 'wer': 'ddd', 'fall': [
    {'1': 'one', '2': 'two'}, {'1': 'uno', '2': 'dos'}]}
b = 5

d1 = date.today().day-2

d2 = date(year=2023, month=12, day=1)

print(d2.strftime("%d/%m/%Y"))
print(d1)
for elems in a['fall']:
    if elems['1'] == 'uno':
        print(elems)

if 10 > b > 3:
    print('yep')


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

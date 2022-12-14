import json
import requests
from config import keys


class APIException(Exception):
    pass
# class Exchange отвечает за конвертацию валюты
class Exchange:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(
                f'Нельзя перевести одинаковые валюты {base}.')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException (f'Не смог обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не смог обработать валюту {base}')

        try:
            amount = int(amount)
        except ValueError:
            raise APIException(f'Не смог обработать количество {amount}')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total_base = float(json.loads(r.content)[keys[quote]]) * amount
        return total_base

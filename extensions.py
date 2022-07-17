import requests
import json

import config

"""
Список доступных к обработке валют
"""
currency = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}

"""
Исключение для ошибок пользователя
"""
class ConversionException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base:str, amount: float) -> float:
        """
        Отправка запроса на сервер конвертации валюты
        """
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
        r_json = json.loads(r.content)
        koeff = r_json[base] * amount
        return f'{koeff} {base} for one {quote}'


if __name__ == '__main__':
    print(Converter.get_price('EUR', 'RUB', 2))
import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class Cryptoconverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if ',' in amount:
            amount = amount.replace(',', '.')  # меняем запятую на точку, если разделителем введена запятая

        try:
            base_label = keys[base][0]
        except KeyError:
            raise ConvertionException(f'Бот не может обработать валюту {base}.Выберите из списка возможных: /values')

        try:
            quote_label = keys[quote][0]
        except KeyError:
            raise ConvertionException(f'Бот не может обработать валюту {quote}.Выберите из списка возможных: /values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}. Введите корректное количество.')
        if amount > 0:
            url = "https://v6.exchangerate-api.com/v6/78763ab1c158ca19b24102f2/latest/"
            curran_base = requests.get(url + base_label)
            curran_base_dict = curran_base.json()
            exchange_rate = curran_base_dict['conversion_rates'].get(quote_label)
            converted_amount = round(amount * exchange_rate, 4)
            return converted_amount, amount  # возвращаем стоимость количества и само количество, проверенное на ошибки
        else:
            raise ConvertionException(f'Не удалось обработать количество {amount}. Введите количество большее 0.')

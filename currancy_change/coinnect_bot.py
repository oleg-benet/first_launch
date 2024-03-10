           # Имя бота "Money Master"
           # Username бота @CoinnectorBot

import telebot
from config import keys, TOKEN
from extension import ConvertionException, Cryptoconverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту через пробел в следующем формате:\n<имя валюты>\
<в какую валюту перевести>\
<количество переводимой валюты>\
\nУвидеть список всех доступных валют: /values')

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:

        values = message.text.lower().split(' ')
        if len(values) != 3:
            raise ConvertionException('Количество параметров не соответствует необходимому')

        base, quote, amount = values

        result = Cryptoconverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        amount = result[1]
        if (amount - int(amount)) == 0:      # если количество валюты с нулевой десятичной частью, в ответе фигурирует
            amount = int(amount)             # целое число без лишних нолей
        if amount == 1 or (amount % 10 == 1 and amount % 100 != 11):  # анализ количества валюты для применения
            decline = keys[base][1]                                   # правильного склонения в ответе
        else:
            decline = keys[base][2]
        text = f'Стоимость {amount} {decline} в {keys[quote][3]} - {result[0]}'
        bot.send_message(message.chat.id, text)


bot.polling()

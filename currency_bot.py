from typing import final
from unittest import expectedFailure
import telebot
import config
from extensions import Converter, ConversionException, currency

TOKEN = config.get_bot_token()

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def command_help(message: telebot.types.Message):
    """
    Обработка команды помощи.
    """
    bot.reply_to(
        message, f'Формат команды: <Имя валюты для перевода> <Имя валюты в которую надо перевести> <Количество перевести>\
        \n(Например: доллар евро 10)\
        Вывести список доступных валют: /values')


@bot.message_handler(commands=['values'])
def command_values(message: telebot.types.Message):
    """
    Обработка команды вывода списка валют.
    """
    answer = ''
    for nick, name in currency.items():
        answer += f' {nick} : {name} \n'
    bot.reply_to(message, f'Currency list:\n{answer}')
    # print(answer)


# Texts
@bot.message_handler(content_types=['text'])
def answer_text(message: telebot.types.Message):
    """
    Обработка текстовых сообщений.
    """
    answer = 'repeat, please'
    try:
        convert_data = is_convert_command_correct(message.text)
        answer = Converter.get_price(**convert_data)
    except ConversionException as ce:
        answer = f'Ошибка пользователя: {str(ce)}'
    except Exception as e:
        answer = f'Не удалось обработать команду.\n{str(e)}'

    bot.reply_to(message, answer)
    # bot.send_message(message.chat.id, answer)


def is_convert_command_correct(message: str):
    """
    Проверяет строку на соответствие формату запроса конвертации валюты.
    В случае любой ошибки выбрасывает исключение.
    """
    result = {}
    parts = message.split(' ')
    # print(f'parts {parts} {parts[2].isdigit()}')
    if len(parts) != 3:
        raise ConversionException(
            'Неверный формат запроса!\nИспользуйте команду /help')

    exception_message = ""
    amount = parts[2]
    if not amount.isdigit():
        exception_message += f'Не верно задано количество конвертации: {amount}\n'
    else:
        amount = int(amount)

    base = parts[0]
    quote = parts[1]

    if base not in currency.keys():
        exception_message += f'Не найдена валюта для перевода: {base}!\n'

    if quote not in currency.keys():
        exception_message += f'Не найдена валюта в которую надо перевести: {quote}!\n'

    if base == quote:
        exception_message += f'Задайте разные валюты {base}\n'

    if exception_message != "":
        raise ConversionException(exception_message)

    result = {'base': currency[base],
              'quote': currency[quote], 'amount': amount}

    return result


# Start bot
bot.polling()

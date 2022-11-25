import telebot
from config import keys, token
from extensions import APIException, Exchange


bot = telebot.TeleBot(token)
# обработчик команды 'start'
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Привет! Я Бот-Конвертер валют и я могу:  ' \
           '\n- Показать список доступных валют через команду /values ' \
           '\n- Вывести конвертацию валюты через команду <имя валюты> ' \
           '<в какую валюту перевести> <количество переводимой валюты>' \
           '\n- Напомнить, что я могу через команду /help'
    bot.reply_to(message, text)

# обработчик команды 'help'
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать конвертацию, введите команду боту в следующем формате:' \
           ' \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>' \
           '\nЧтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)

# обработчик команды 'values'
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

# обработчик любой команды от пользователя
@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException ('Введите команду или 3 параметра')

        base, quote, amount = values
        total_base = Exchange.get_price(quote, base, amount)
    except APIException  as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}')
    else:
        text = f'Переводим {keys[base]} в {keys[quote]}\n{amount} {keys[base]} = {total_base} {keys[quote]}'
        bot.send_message(message.chat.id, text)


bot.polling()
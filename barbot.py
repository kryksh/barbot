import telebot
from telebot import types
import funcs

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    msg = bot.send_message(message.chat.id, 'Доступные команды:\n/help - показывает это сообщение;\n/bars - показать ближайшие бары.')


@bot.message_handler(commands=['bars'])
def bars(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True, resize_keyboard=True)
    button_loc = types.KeyboardButton(text='Отправить местоположение', request_location=True)
    keyboard.add(button_loc)
    msg = bot.send_message(message.chat.id, 'Пришли свое местоположение и я покажу адреса ближайших баров.', reply_markup=keyboard)


@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        keyboard = types.ReplyKeyboardRemove()
        l = (message.location.longitude, message.location.latitude)
        mes = funcs.get_bars(location=l)
        for x in mes:
            msg = bot.send_message(message.chat.id, x, reply_markup=keyboard)


bot.polling()
import telebot
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import text
import psycopg2

class Ren_bot:
    def __init__(self, url):
        self.bot = telebot.TeleBot(url)
        self.conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')

    def start(self):
# создание кнопок для бота
        @self.bot.message_handler(commands = ['start'])
        def start_screen(message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            with self.conn.connect() as connection:
                response_credit = connection.execute(text('SELECT * FROM credit_cards'))
                data_credit = response_credit.fetchall()
                if (len(data_credit[0]) != 0):
                    btn1 = types.KeyboardButton("Кредитные карты")
                    markup.add(btn1)

                response_debit = connection.execute(text('SELECT * FROM debit_cards'))
                data_debit = response_debit.fetchall()
                if (len(data_debit[0]) != 0):
                    btn2 = types.KeyboardButton("Дебетовые карты")
                    markup.add(btn2)
            self.bot.send_message(message.chat.id,
                                  text="Привет, {0.first_name}! Этот бот ознакомит Вас с продуктами Ренессанс банка!".format(
                                      message.from_user), reply_markup=markup)

            # варианты предложений для каждой кнопки (для каждого направления)
            @self.bot.message_handler(content_types=['text'])
            def func(message):
                i = 0
                if (message.text == "Кредитные карты"):
                    i += 1
                    self.bot.send_message(message.chat.id,
                                          text=data_credit[i][1].format(
                                              message.from_user), reply_markup=markup)

                    # обработчик инлайн кнопок

            @self.bot.callback_query_handler(func=lambda call: True)
            def callback_query(call):
                req = call.data.split('_')
                if req[0] == 'сredit_cards_offer':
                    i = 0
                    for row in data_credit:
                        i += 1
                        self.bot.send_message(call.message.chat.id, data_credit[i][1], parse_mode="html")

        self.bot.polling(none_stop=True)


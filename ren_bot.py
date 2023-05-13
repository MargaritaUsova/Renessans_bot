import telebot
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy import text
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

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
                response_buttons = connection.execute(text('SELECT * FROM buttons'))
                data_buttons = response_buttons.fetchall()
                btns = []
                if (len(data_buttons[0]) != 0):
                    for k in range(len(data_buttons)):
                        if data_buttons[k][3]:
                            btn = types.KeyboardButton(data_buttons[k][1])
                            btns.append(btn)
                            markup.add(btn)
                            response_credit = connection.execute(text('SELECT * FROM credit_cards'))
                            data_credit = response_credit.fetchall()
                            response_debit = connection.execute(text('SELECT * FROM debit_cards'))
                            data_debit = response_debit.fetchall()
                btn3 = types.KeyboardButton('Поддержка')
                markup.add(btn3)

            self.bot.send_message(message.chat.id,
                                  text="Привет, {0.first_name}! Этот бот ознакомит Вас с продуктами Ренессанс банка!".format(
                                      message.from_user), reply_markup=markup)

            # варианты предложений для каждой кнопки (для каждого направления)
            @self.bot.message_handler(content_types=['text'])
            def func(message):
                if (message.text == "Кредитные карты"):
                    credit_cards_info = ''
                    for k in range(len(data_credit)):
                        if data_credit[k][3]:
                            credit_cards_info += '<b>' + data_credit[k][1] + '</b>' + '\n'
                            credit_cards_info += data_credit[k][2] + '\n' + '\n'
                    self.bot.send_message(message.chat.id,
                                              text=f'{credit_cards_info}'.format(
                                                  message.from_user), reply_markup=markup, parse_mode="html")

                elif (message.text == 'Дебетовые карты'):
                    debit_cards_info = ''
                    for k in range(len(data_debit)):
                        if data_debit[k][3]:
                            debit_cards_info += '<b>' + data_debit[k][1] + '</b>' + '\n'
                            debit_cards_info += data_debit[k][2] + '\n' + '\n'
                    self.bot.send_message(message.chat.id,
                                          text=f'{debit_cards_info}'.format(
                                              message.from_user), reply_markup=markup, parse_mode="html")

                elif (message.text == 'Поддержка'):
                    self.bot.send_message(message.chat.id,
                                          text="Введите тему обращения : \n".format(
                                              message.from_user), reply_markup=markup)
                    #connection.execute(f"INSERT INTO support (appeal_theme) VALUES ({message.text})")
                    #connection.commit()

                    markup_support = InlineKeyboardMarkup()
                    #markup_support.add(InlineKeyboardButton(text='Кредит на любые цели', callback_data='сredit4everything'))
                    #markup_support.add(InlineKeyboardButton(text='Рефинансирование кредита', callback_data='refinance'))
                    #markup_support.add(InlineKeyboardButton(text='Кредиты на покупку товаров', callback_data='сredit4products'))


        self.bot.polling(none_stop=True)


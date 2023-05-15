import telebot
import psycopg2
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy import text

class Ren_bot:
    def __init__(self, url):
        self.bot = telebot.TeleBot(url)
        self.conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')

    def start(self):
# создание кнопок для бота
        @self.bot.message_handler(commands = ['start'])
        def start_screen(message):
            self.markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

            with self.conn.connect() as connection:
                response_buttons = connection.execute(text('SELECT * FROM buttons'))
                data_buttons = response_buttons.fetchall()
                btns = []
                if (len(data_buttons[0]) != 0):
                    for k in range(len(data_buttons)):
                        if data_buttons[k][3]:
                            btn = types.KeyboardButton(data_buttons[k][1])
                            btns.append(btn)

                            response_credit = connection.execute(text('SELECT * FROM credit_cards'))
                            self.data_credit = response_credit.fetchall()
                            response_debit = connection.execute(text('SELECT * FROM debit_cards'))
                            self.data_debit = response_debit.fetchall()
                            response_offers = connection.execute(text('SELECT * FROM special_offers'))
                            self.data_offers = response_offers.fetchall()
                self.markup.add(*btns)
                btn3 = types.KeyboardButton('Поддержка')
                self.markup.add(btn3)

            self.bot.send_message(message.chat.id,
                                  text="Привет, {0.first_name}! Этот бот ознакомит Вас с продуктами Ренессанс банка!".format(
                                      message.from_user), reply_markup=self.markup)
            self.conn.execute(
                f'insert into users (id) select {message.from_user.id} where not exists ( select id from users where id = {message.from_user.id})')




        def get_theme_appeal(message):
            global theme
            theme = message.text
            self.bot.send_message(message.from_user.id, 'Введите свою фамилию : \n')
            self.bot.register_next_step_handler(message, get_surname)

        def get_surname(message):
            global surname
            surname = message.text
            self.bot.send_message(message.from_user.id, 'Введите свое имя : \n')
            self.bot.register_next_step_handler(message, get_name)

        def get_name(message):
            global name
            name = message.text
            self.bot.send_message(message.from_user.id, 'Введите свое отчество : \n')
            self.bot.register_next_step_handler(message, get_patronymic)

        def get_patronymic(message):
            global patronymic
            patronymic = message.text
            self.bot.send_message(message.from_user.id, 'Введите свой номер телефона : \n')
            self.bot.register_next_step_handler(message, get_phone_num)

        def get_phone_num(message):
            global phone_num
            phone_num = message.text
            self.bot.send_message(message.from_user.id, 'Введите свой Email: \n')
            self.bot.register_next_step_handler(message, get_email)

        def get_email(message):
            global email
            email = message.text
            self.bot.send_message(message.from_user.id, 'Введите свой регион : \n')
            self.bot.register_next_step_handler(message, get_region)


        def get_region(message):
            global region
            region = message.text
            self.bot.send_message(message.from_user.id, 'Введите текст своего обращения : \n')
            self.bot.register_next_step_handler(message, get_text)

        def get_text(message):
            global text
            text = message.text
            self.bot.send_message(message.from_user.id, 'Введите номер договора (если есть)')
            self.bot.register_next_step_handler(message, get_appeal_num)

        def get_appeal_num(message):
            global appeal_num
            appeal_num = message.text

            to_db()
        def to_db():
            conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')
            conn.execute(f'insert into support (theme, surname, name, patronymic, phone_num, email, region, text, appeal_num)' +
             f'values (\'{theme}\', \'{surname}\', \'{patronymic}\', \'{name}\', \'{phone_num}\', \'{email}\', \'{region}\', \'{text}\', \'{appeal_num}\')')


            # варианты предложений для каждой кнопки (для каждого направления)
        @self.bot.message_handler(content_types=['text'])
        def func(message):
            if (message.text == "Кредитные карты"):
                credit_cards_info = ''
                for k in range(len(self.data_credit)):
                    if self.data_credit[k][3]:
                        credit_cards_info += '<b>' + self.data_credit[k][1] + '</b>' + '\n'
                        credit_cards_info += self.data_credit[k][2] + '\n' + '\n'
                self.bot.send_message(message.chat.id,
                                          text=f'{credit_cards_info}'.format(
                                              message.from_user), reply_markup=self.markup, parse_mode="html")
                sql = "INSERT INTO user_clicks  (id, button_name) VALUES (%s, %s)"
                conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')
                values = (message.chat.id, 'Кредитные карты')
                conn.execute(sql, values)

            elif (message.text == 'Дебетовые карты'):
                #@self.bot.
                debit_cards_info = ''
                for k in range(len(self.data_debit)):
                    if self.data_debit[k][3]:
                        debit_cards_info += '<b>' + self.data_debit[k][1] + '</b>' + '\n'
                        debit_cards_info += self.data_debit[k][2] + '\n' + '\n'
                self.bot.send_message(message.chat.id,
                                      text=f'{debit_cards_info}'.format(
                                          message.from_user), reply_markup=self.markup, parse_mode="html")
                sql = "INSERT INTO user_clicks  (id, button_name) VALUES (%s, %s)"
                conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')
                values = (message.chat.id, 'Дебетовые карты')
                conn.execute(sql, values)

            elif (message.text == 'Поддержка'):
                self.bot.send_message(message.from_user.id, 'Введите тему обращения : \n')
                self.bot.register_next_step_handler(message, get_theme_appeal)
            elif (message.text == 'Спецпредложения'):
                data_offers_info = ''
                for k in range(len(self.data_offers)):
                    if self.data_offers[k][3]:
                        data_offers_info += '<b>' + self.data_offers[k][1] + '</b>' + '\n'
                        data_offers_info += self.data_offers[k][2] + '\n' + '\n'
                self.bot.send_message(message.chat.id,
                                      text=f'{data_offers_info}'.format(
                                          message.from_user), reply_markup=self.markup, parse_mode="html")
                sql = "INSERT INTO user_clicks  (id, button_name) VALUES (%s, %s)"
                conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')
                values = (message.chat.id, 'Дебетовые карты')
                conn.execute(sql, values)

        self.bot.polling(none_stop=True)


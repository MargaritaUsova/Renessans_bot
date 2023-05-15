from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import text
import psycopg2

conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')

with conn.connect() as connection:
    response = connection.execute(text('SELECT * FROM credit_cards'))
    data = response.fetchall()
    for row in data:
        pass

with conn.connect() as connection:
    response_buttons = connection.execute(text('SELECT * FROM buttons'))
    data_buttons = response_buttons.fetchall()
    #print(response_credit['text'].value_counts())
    #print(data_buttons[0][3])

sql = "INSERT INTO support (theme,surname,patronymic,phone_num,email,region,text,appeal_num) " \
                  "VALUES (%s, %s,%s,%s,%s,%s, %s,%s, %s)"
values = ('theme', 'surname}', '{patronymic}', '{phone_num}', '{email}', '{region}', '{text}',
'{appeal_num}')

conn = create_engine('postgresql://admin:HackYeah13b20Women@185.86.146.143:5432/RenDB')
sql = "INSERT INTO support (theme,surname,patronymic,phone_num,email,region,text,appeal_num) VALUES (%s, %s,%s,%s,%s,%s, %s,%s,%s,%s)"
values = ('theme', 'surname}', '{patronymic}', '{phone_num}', '{email}', '{region}', '{text}',
'{appeal_num}')
conn.execute(sql, values)



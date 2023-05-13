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
    response_credit = connection.execute(text('SELECT * FROM credit_cards'))
    data_credit = response_credit.fetchall()
    print(data_credit[0][1])


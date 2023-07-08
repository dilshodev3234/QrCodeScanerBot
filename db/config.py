import os
import psycopg2
import sqlite3
from dotenv import load_dotenv

load_dotenv()


class DB:
    # con = psycopg2.connect(
    #     dbname=os.getenv('DB_NAME'),
    #     user=os.getenv('DB_USER'),
    #     password=os.getenv('DB_PASSWORD'),
    #     host=os.getenv('DB_HOST'),
    #     port=os.getenv("DB_PORT"),
    # )
    con = sqlite3.connect("/root/QrCodeScanerBot/db/project.sqlite")

    cur = con.cursor()

    table1 = """create table if not exists qrcodes(
        id integer primary key,
        active bool
    );"""

    table2 = """create table if not exists users(
        id integer primary key autoincrement,
        user_id varchar(255),
        name varchar(50),
        phone varchar(50),
        qrcode_id integer,
        created_at timestamp default current_timestamp
    );"""
    cur.execute(table1)
    cur.execute(table2)
    con.commit()

    def select(self, qr_code_id):
        fields = ','.join(self.fields) if self.fields else '*'
        table_name = self.__class__.__name__.lower()
        query = f"""select {fields} from {table_name} where id=?"""
        self.cur.execute(query , (qr_code_id,))
        return self.cur

    def insert_into(self, **params):
        fields = ','.join(params.keys())
        values = tuple(params.values())
        table_name = self.__class__.__name__.lower()
        query = f"""insert into {table_name}({fields}) values ({','.join(['?'] * len(params))})"""
        self.cur.execute(query, values)
        self.con.commit()

    def update(self, qrcode_id: str, **kwargs):
        table_name = self.__class__.__name__.lower()
        f = list(kwargs.keys())
        f.append(' ')
        set_fields = " = ?,".join(f).strip(', ')
        params = list(kwargs.values())
        params.append(qrcode_id)
        query = f"""update {table_name} set {set_fields} where id=?"""
        self.cur.execute(query, params)
        self.con.commit()

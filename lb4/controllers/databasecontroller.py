from datetime import datetime
import sqlite3


class CurrencyRatesCrud:
    def __init__(self, currency_rates_obj):
        self.__con = sqlite3.connect('data.sqlite3')
        self.__cursor = self.__con.cursor()
        self.__currency_rates_obj = currency_rates_obj
        self.__create_table()

    def __create_table(self):
        self.__con.execute(
            "CREATE TABLE IF NOT EXISTS currency("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "cur TEXT,"
            "date TEXT,"
            "value FLOAT);"
        )
        self.__con.commit()

    def create(self):
        rates = self.__currency_rates_obj.get_rates()
        params = [
            {"cur": code, "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "value": rate}
            for code, rate in rates.items()
        ]
        self.__cursor.executemany(
            "INSERT INTO currency(cur, date, value) VALUES(:cur, :date, :value)",
            params
        )
        self.__con.commit()

    def read(self, code=None):
        if code:
            self.__cursor.execute("SELECT * FROM currency WHERE cur = :code", {"code": code})
        else:
            self.__cursor.execute("SELECT * FROM currency")
        return self.__cursor.fetchall()

    def update(self, code, new_value):
        self.__cursor.execute(
            "UPDATE currency SET value = :value WHERE cur = :code",
            {"code": code, "value": new_value}
        )
        self.__con.commit()

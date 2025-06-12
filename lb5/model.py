import requests
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

Base = declarative_base()

class CurrencyRate(Base):
    __tablename__ = 'currency_rates'
    id = Column(String(3), primary_key=True)
    datetime = Column(String(20))
    value = Column(Float)


class CurrencyRatesSingleton:
    _instance = None

    def __new__(cls, db_url="sqlite:///database.db"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_db(db_url)
            cls._instance.tracked_currencies = ['USD', 'EUR']
        return cls._instance

    def _init_db(self, db_url):
        self.engine = create_engine(db_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def fetch_rates(self):
        url = 'https://www.cbr.ru/scripts/XML_daily.asp'
        response = requests.get(url)
        tree = ET.fromstring(response.content)
        now = datetime.now().strftime('%d-%m-%Y %H:%M')
        rates = {}

        for valute in tree.findall('Valute'):
            code = valute.find('CharCode').text
            if code in self.tracked_currencies:
                value = float(valute.find('Value').text.replace(',', '.'))
                rates[code] = {'datetime': now, 'value': value}

        session = self.Session()
        for code, data in rates.items():
            rate = session.query(CurrencyRate).get(code)
            if not rate:
                rate = CurrencyRate(id=code)
                session.add(rate)
            rate.datetime = data['datetime']
            rate.value = data['value']
        session.commit()
        session.close()

    def get_rates(self):
        session = self.Session()
        rates = session.query(CurrencyRate).all()
        session.close()
        return rates

    def set_tracked(self, currency_codes):
        self.tracked_currencies = currency_codes
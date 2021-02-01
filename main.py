from fastapi import FastAPI
import datetime
from pydantic import BaseModel
storage = {}
app = FastAPI()

@app.get('/')
def home():
    return {'key':'hello'}

@app.get('/{pk}')
def get_item(pk:int, q: int=None):
    return {'key': pk, 'q': q}

@app.get('/currency/{currency_code}/date/{currency_date}/')
def get_currency(currency_code:str, date: datetime.date=datetime.datetime.now().date()):
    return storage[currency_code][date]

class CurrencyRate(BaseModel):
    rate: float
    currency_date: datetime.date=datetime.datetime.now().date()


@app.post('/currency/{currency_code}')
def post(currency_code:str, currency_rate: CurrencyRate):
    print('currency_code', currency_code)
    print('currency_rate.currency_date', currency_rate.currency_date)
    print('currency_rate.rate', currency_rate.rate)
    storage[currency_code][currency_rate.currency_date] = currency_rate.rate
    return  currency_rate








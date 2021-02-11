from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from all_currencies import all_currencies
from currency import Currency
import time

storage = {}
app = FastAPI()


class CurrencyRate(BaseModel):
    rate: float
    currency_date: datetime = None


def check_date(date):
    if date is None:
        return datetime.now()
    return date


@app.get('/')
async def read_main():
    return {"msg": "Hi! I am little but very myself proud HTTP currency exchange server"}


@app.post('/post/currency/{currency_code}')
def post_currency_with_date(currency_code: str, currency_rate: CurrencyRate):
    date = check_date(currency_rate.currency_date)
    if currency_rate.rate <= 0 or currency_code not in all_currencies:
        return {'error': 'Currency rate should be bigger than 0, currency_code should be in follow format: '
                         'AUD, RUB, USD, EUR'}
    if currency_code in storage:
        storage[currency_code].add_rate(currency_rate.rate, date)
    else:
        storage[currency_code] = Currency(currency_code, currency_rate.rate, date)
    return {'currency_code': currency_code, 'currency_rate': currency_rate.rate, 'date': date}


@app.get('/get/currency/{currency_code}/')
@app.get('/get/currency/{currency_code}/date/{date}/')
def get_currency(currency_code: str, date: datetime = None):
    date = check_date(date)
    if currency_code in storage:
        rate = storage[currency_code].get_rate(date)
        update = storage[currency_code].get_date(rate)
        return {'currency_code': currency_code, 'currency_rate': rate, 'since': update}
    else:
        return {'error': 'Sorry, there is no info about ' + currency_code + ' rate'}


@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/')
@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/date/{date}')
def get_rate_for_pair(from_currency_code: str, to_currency_code: str, date: datetime = None):
    date = check_date(date)
    if from_currency_code in storage and to_currency_code in storage:
        from_rate = storage[from_currency_code].get_rate(date)
        to_rate = storage[to_currency_code].get_rate(date)
        rate = from_rate / to_rate
        return {'1 ' + from_currency_code: str(rate) + ' ' + to_currency_code}
    else:
        return {'error': 'I do not have enough information for your request'}

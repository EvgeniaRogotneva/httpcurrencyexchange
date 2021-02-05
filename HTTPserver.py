from fastapi import FastAPI
import datetime
from pydantic import BaseModel
from all_currencies import all_currencies
storage = {}
app = FastAPI()


class CurrencyRate(BaseModel):
    rate: float
    currency_date: datetime.date = datetime.date.today()


@app.get('/')
async def read_main():
    return {"msg": "Hi! I am little but very myself proud HTTP currency exchange server"}


@app.post('/post/currency/{currency_code}')
def post(currency_code: str, currency_rate: CurrencyRate):
    if currency_rate.rate > 0 and currency_code in all_currencies:
        storage[currency_code] = {currency_rate.currency_date: currency_rate.rate}
        return {'currency_code': currency_code, 'currency_rate': currency_rate.rate, 'date': currency_rate.currency_date}
    else:
        return {'error': 'Currency rate should be bigger than 0, currency_code should be in follow format: '
                         'AUD, RUB, USD, EUR'}


@app.get('/get/currency/{currency_code}/')
@app.get('/get/currency/{currency_code}/date/{date}/')
def get_currency(currency_code: str, date: datetime.date = datetime.date.today()):
    if currency_code in storage and date in storage[currency_code]:
        return {'currency_code': currency_code, 'currency_rate': storage[currency_code][date], 'date': date}
    else:
        return {'error': 'Sorry, there is no info about ' + currency_code + ' ' + str(date) + ' rate'}


@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/')
@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/date/{date}')
def get_rate_for_pair(from_currency_code: str, to_currency_code: str, date: datetime.date = datetime.date.today()):
    if from_currency_code in storage and to_currency_code in storage:
        if date in storage[from_currency_code] and date in storage[to_currency_code]:
            rate = storage[from_currency_code][date] / storage[to_currency_code][date]
            return {'1 ' + from_currency_code: str(rate) + ' ' + to_currency_code, 'date': date}
    else:
        return {'error': 'I do not have enough information for your request'}

from fastapi import FastAPI
import datetime
from pydantic import BaseModel
storage = {}
app = FastAPI()


class CurrencyRate(BaseModel):
    rate: float
    currency_date: datetime.date = datetime.date.today()


@app.post('/post/currency/{currency_code}')
def post(currency_code: str, currency_rate: CurrencyRate):
    storage[currency_code] = {currency_rate.currency_date: currency_rate.rate}
    return storage[currency_code]


@app.get('/get/currency/{currency_code}/')
@app.get('/get/currency/{currency_code}/date/{date}/')
def get_currency(currency_code: str, date: datetime.date = datetime.date.today()):
    if currency_code in storage and date in storage[currency_code]:
        return storage[currency_code][date]
    else:
        return 'Sorry, there is no info about' + currency_code + date + 'rate'


@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/')
@app.get('/get/from/{from_currency_code}/to/{to_currency_code}/date/{date}')
def get_rate_for_pair(from_currency_code: str, to_currency_code: str, date: datetime.date = datetime.date.today()):
    if from_currency_code in storage and to_currency_code in storage:
        if date in storage[from_currency_code] and date in storage[to_currency_code]:
            rate = storage[from_currency_code][date] / storage[to_currency_code][date]
            return rate
    else:
        return 'I do not have enough information for your request'

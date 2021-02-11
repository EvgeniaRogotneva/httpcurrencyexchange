import unittest
from HTTPserver import app
from HTTPserver import storage
from starlette.testclient import TestClient
import requests
from datetime import datetime
import json


class TestCurrencyExchange(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        storage.clear()

    def test_get_main(self):
        with TestClient(app) as client:
            response = client.get('/')
            assert response.status_code == 200
            assert response.json() == {"msg": "Hi! I am little but very myself proud HTTP currency exchange server"}

    def test_add_currency(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                                    "rate": 58.0284,
                                    "currency_date": '2021-02-11T09:29:31.935000+00:00'})
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284,
                                       "date": '2021-02-11T09:29:31.935000+00:00'}

    def test_get_currency_rate(self):
        with TestClient(app) as client:
            time = datetime.now().isoformat()
            response = client.post("/post/currency/AUD", json={
                "rate": 58.0284,
                "currency_date": time})
            assert response.status_code == 200
            response = client.get('/get/currency/AUD')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284,
                                       "since": time}

    def test_get_currency_rate_with_date(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                "rate": 58.0284,
                "currency_date": "2021-02-11T09:29:31.935000+00:00"})
            assert response.status_code == 200
            response = client.get('/get/currency/AUD/date/2021-02-11T09:29:31.935000+00:00')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284,
                                       "since": "2021-02-11T09:29:31.935000+00:00"}

    def test_get_rate_for_pair(self):
        with TestClient(app) as client:
            time = datetime.today().isoformat()
            '''post currency's rates'''
            response = client.post("/post/currency/EUR", json={"rate": 91.5624,
                                                               "currency_date": time})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 76.0801,
                                                               "currency_date": time})
            assert response.status_code == 200

            '''get currency's rate'''
            response = client.get('/get/from/EUR/to/USD')
            assert response.status_code == 200
            assert response.json() == {'1 EUR': '1.2034999953995853 USD'}
            response = client.get('/get/from/USD/to/EUR')
            assert response.status_code == 200
            assert response.json() == {'1 USD': '0.8309098494578561 EUR'}

    def test_get_rate_for_pair_with_date(self):
        with TestClient(app) as client:
            '''post currency's rates'''
            response = client.post("/post/currency/EUR", json={"rate": 91.5624,
                                                               "currency_date": "2021-02-11T09:29:31.935000+00:00"})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 76.0801,
                                                               "currency_date": "2021-02-11T09:29:31.935000+00:00"})
            assert response.status_code == 200

            '''get currency's rate for pair with date'''
            response = client.get('/get/from/EUR/to/USD/date/2021-02-11T09:29:31.935000+00:00')
            assert response.status_code == 200
            assert response.json() == {'1 EUR': '1.2034999953995853 USD'}
            response = client.get('/get/from/USD/to/EUR/date/2021-02-11T09:29:31.935000+00:00')
            assert response.status_code == 200
            assert response.json() == {'1 USD': '0.8309098494578561 EUR'}

    def test_add_currency_wrong_format(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/123", json={
                                    "rate": 58.0284,
                                    "currency_date": "2021-02-11T09:29:31.935000+00:00"})
            assert response.status_code == 200
            assert response.json() == {'error': 'Currency rate should be bigger than 0, '
                                                'currency_code should be in follow format: AUD, RUB, USD, EUR'}

    def test_get_currency_rate_from_empty_server(self):
        with TestClient(app) as client:
            response = client.get('/get/currency/AUD')
            assert response.status_code == 200
            assert response.json() == {'error': 'Sorry, there is no info about AUD rate'}

    def test_get_currency_rate_with_date_from_empty_server(self):
        with TestClient(app) as client:
            response = client.get('/get/currency/AUD/date/2021-02-11T09:29:31.935000+00:00')
            assert response.status_code == 200
            assert response.json() == {'error': 'Sorry, there is no info about AUD rate'}

    def test_get_rate_for_pair_from_empty_server(self):
        with TestClient(app) as client:
            '''get currency's rate'''
            response = client.get('/get/from/EUR/to/USD')
            assert response.status_code == 200
            assert response.json() == {'error': 'I do not have enough information for your request'}

    def test_post_zero_rate(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                "rate": 0,
                "currency_date": "2021-02-11T09:29:31.935000+00:00"})
            assert response.status_code == 200
            assert response.json() == {'error': 'Currency rate should be bigger than 0, '
                                                'currency_code should be in follow format: AUD, RUB, USD, EUR'}

    def test_check_correct_additional_two_dates(self):
        with TestClient(app) as client:
            '''post currency's rates'''
            response = client.post("/post/currency/USD", json={"rate": 100,
                                                               "currency_date": "2021-02-10T09:29:31.935000+00:00"})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 50,
                                                               "currency_date": "2021-02-05T09:29:31.935000+00:00"})
            assert response.status_code == 200

            response = client.get('/get/currency/USD/date/2021-02-10T09:29:31.935000+00:00')
            assert response.status_code == 200

            assert response.json() == {"currency_code": "USD", "currency_rate": 100,
                                       "since": "2021-02-10T09:29:31.935000+00:00"}

            response = client.get('/get/currency/USD/date/2021-02-05T09:29:31.935000+00:00')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "USD", "currency_rate": 50,
                                       "since": "2021-02-05T09:29:31.935000+00:00"}

    def test_for_pair_with_ruble(self):
        with TestClient(app) as client:
            time = datetime.now().isoformat()
            '''post currency's rates'''
            response = client.post("/post/currency/EUR", json={"rate": 91.5624,
                                                               "currency_date": time})
            assert response.status_code == 200
            response = client.post("/post/currency/RUB", json={"rate": 1,
                                                               "currency_date": time})
            assert response.status_code == 200

            '''get currency's rate'''
            response = client.get('/get/from/EUR/to/RUB')
            assert response.status_code == 200
            print('response',response.json())
            print({'1 EUR': '91.5624 RUB', 'date': time})
            assert response.json() == {'1 EUR': '91.5624 RUB'}
            response = client.get('/get/from/RUB/to/EUR')
            assert response.status_code == 200
            print('response',response.json())
            assert response.json() == {'1 RUB': '0.010921513634417622 EUR'}

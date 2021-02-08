import unittest
from HTTPserver import app
from HTTPserver import storage
from starlette.testclient import TestClient
import requests
import datetime


class TestCurrencyExchange(unittest.TestCase):

    def setUp(self) -> None:
        storage.clear()

    def tearDown(self) -> None:
        pass

    def test_get_main(self):
        with TestClient(app) as client:
            response = client.get('/')
            assert response.status_code == 200
            assert response.json() == {"msg": "Hi! I am little but very myself proud HTTP currency exchange server"}

    def test_add_currency(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                                    "rate": 58.0284,
                                    "currency_date": "2021-02-03"})
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284, "date": "2021-02-03"}
        self.tearDown()

    def test_get_currency_rate(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                "rate": 58.0284,
                "currency_date": str(datetime.date.today())})
            assert response.status_code == 200
            response = client.get('/get/currency/AUD')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284,
                                       "date": str(datetime.date.today())}
        self.tearDown()

    def test_get_currency_rate_with_date(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                "rate": 58.0284,
                "currency_date": "2021-02-03"})
            assert response.status_code == 200
            response = client.get('/get/currency/AUD/date/2021-02-03')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "AUD", "currency_rate": 58.0284,
                                       "date": "2021-02-03"}
        self.tearDown()

    def test_get_rate_for_pair(self):
        with TestClient(app) as client:
            '''post currency's rates'''
            response = client.post("/post/currency/EUR", json={"rate": 91.5624,
                                                               "currency_date": str(datetime.date.today())})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 76.0801,
                                                               "currency_date": str(datetime.date.today())})
            assert response.status_code == 200

            '''get currency's rate'''
            response = client.get('/get/from/EUR/to/USD')
            assert response.status_code == 200
            assert response.json() == {'1 EUR': '1.2034999953995853 USD', 'date': str(datetime.date.today())}
            response = client.get('/get/from/USD/to/EUR')
            assert response.status_code == 200
            assert response.json() == {'1 USD': '0.8309098494578561 EUR', 'date': str(datetime.date.today())}
        self.tearDown()

    def test_get_rate_for_pair_with_date(self):
        with TestClient(app) as client:
            '''post currency's rates'''
            response = client.post("/post/currency/EUR", json={"rate": 91.5624,
                                                               "currency_date": "2021-02-05"})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 76.0801,
                                                               "currency_date": "2021-02-05"})
            assert response.status_code == 200

            '''get currency's rate for pair with date'''
            response = client.get('/get/from/EUR/to/USD/date/2021-02-05')
            assert response.status_code == 200
            assert response.json() == {'1 EUR': '1.2034999953995853 USD', 'date': '2021-02-05'}
            response = client.get('/get/from/USD/to/EUR/date/2021-02-05')
            assert response.status_code == 200
            assert response.json() == {'1 USD': '0.8309098494578561 EUR', 'date': '2021-02-05'}

        self.tearDown()



    def test_add_currency_wrong_format(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/123", json={
                                    "rate": 58.0284,
                                    "currency_date": "2021-02-03"})
            assert response.status_code == 200
            assert response.json() == {'error': 'Currency rate should be bigger than 0, '
                                                'currency_code should be in follow format: AUD, RUB, USD, EUR'}
        self.tearDown()

    def test_get_currency_rate_from_empty_server(self):
        with TestClient(app) as client:
            response = client.get('/get/currency/AUD')
            assert response.status_code == 200
            assert response.json() == {'error': 'Sorry, there is no info about AUD '
                                                + str(datetime.date.today()) + ' rate'}
        self.tearDown()

    def test_get_currency_rate_with_date_from_empty_server(self):
        with TestClient(app) as client:
            response = client.get('/get/currency/AUD/date/2021-02-03')
            assert response.status_code == 200
            assert response.json() == {'error': 'Sorry, there is no info about AUD 2021-02-03 rate'}
        self.tearDown()

    def test_get_rate_for_pair_from_empty_server(self):
        with TestClient(app) as client:
            '''get currency's rate'''
            response = client.get('/get/from/EUR/to/USD')
            assert response.status_code == 200
            assert response.json() == {'error': 'I do not have enough information for your request'}
        self.tearDown()

    def test_post_zero_rate(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                "rate": 0,
                "currency_date": "2021-02-03"})
            assert response.status_code == 200
            assert response.json() == {'error': 'Currency rate should be bigger than 0, '
                                                'currency_code should be in follow format: AUD, RUB, USD, EUR'}
        self.tearDown()

    def test_check_correct_additional_two_dates(self):
        with TestClient(app) as client:
            '''post currency's rates'''
            response = client.post("/post/currency/USD", json={"rate": 80.5624,
                                                               "currency_date": "2021-02-06"})
            assert response.status_code == 200
            response = client.post("/post/currency/USD", json={"rate": 76.0801,
                                                               "currency_date": "2021-02-05"})
            assert response.status_code == 200

            response = client.get('/get/currency/USD/date/2021-02-06')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "USD", "currency_rate": 80.5624,
                                       "date": "2021-02-06"}

            response = client.get('/get/currency/USD/date/2021-02-05')
            assert response.status_code == 200
            assert response.json() == {"currency_code": "USD", "currency_rate": 76.0801,
                                       "date": "2021-02-05"}



import unittest
from HTTPserver import app
from starlette.testclient import TestClient
import requests




class TestCurrencyExchange(unittest.TestCase):
    def setUp(self) -> None:
        pass



    def test_get_main(self):
        with TestClient(app) as client:
            response = client.get('/')
            assert response.status_code == 200
            assert response.json() == {"msg": "Hello World"}

    def test_add_currency(self):
        with TestClient(app) as client:
            response = client.post("/post/currency/AUD", json={
                                    "rate": 58.0284,
                                    "currency_date": "2021-02-03"})
            print(response)
            print(response.status_code)
            print(response.json())




    def test_add_currency_with_date(self):
        pass


    def test_get_currency_rate(self):
        pass


    def test_get_currency_rate_with_date(self):
        pass


    def test_get_rate_for_pair(self):
        pass


    def test_add_currency_wrong_format(self):
        pass


    def test_get_currency_rate_from_empty_server(self):
        pass


    def test_get_rate_for_pair_from_empty_server(self):
        pass


    def test_post_zero_rate(self):
        pass


    def tearDown(self) -> None:
        pass

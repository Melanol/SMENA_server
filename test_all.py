"""Execute with "pytest" in-console on this folder."""
import json

import requests


class TestClass:
    def test_create_checks(self):
        order = {
                "id": 3000,
                "price": 1000,
                "address": "Уфа, Ленина 9000",
                "client": {
                    "name": "Иванов Иван",
                    "phone": "9173430000"
                },
                "items": [
                    {
                        "name": "Пицца",
                        "quantity": 1,
                        "unit_price": 500
                    },
                    {
                        "name": "Ролл",
                        "quantity": 1,
                        "unit_price": 500
                    }
                ],
                "point_id": 1}
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:8000/create_checks/',
                          data=json.dumps(order), headers=headers)
        print(response.text)
        assert False

    def test_new_checks(self):
        headers = {'Content-Type': 'application/json'}
        response = requests.get('http://localhost:8000/new_checks/',
                                 headers=headers, params={'api_key': 'key1'})
        print(response.text)
        assert False

    def test_check(self):
        headers = {'Content-Type': 'application/json'}
        response = requests.get('http://localhost:8000/check/',
                                 headers=headers, params={'api_key': 'key1',
                                                          'check_id': 1})
        print(response.text)
        assert False

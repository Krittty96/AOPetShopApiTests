import allure
import jsonschema
import requests
import pytest
from requests.compat import integer_types

from .schemas.inventory_petshop_schema import INVENTORY_PETSHOP_SCHEMA
from .schemas.order_schema import ORDER_SCHEMA

BASE_URL = 'http://5.181.109.28:9090/api/v3'


@allure.feature('Store')
class TestStorePetShop:
    @allure.title("Размещение заказа")
    def test_creating_an_order(self, create_an_order):
        payload = create_an_order
        with allure.step('Отправка запроса с телом'):
            response = requests.post(url=f'{BASE_URL}/store/order', json=payload)
        with allure.step('Проверка кода ответа и валидация JSON-схемы'):
            assert response.status_code == 200
            jsonschema.validate(response.json(), ORDER_SCHEMA)

        with allure.step('Проверка параметров заказа в ответе'):
            assert response.json()['id'] == payload['id'], 'ID заказа не совпадает с ожидаемым'
            assert response.json()['petId'] == payload['petId'], 'petId не совпадает с ожидаемым'
            assert response.json()['quantity'] == payload['quantity'], 'quantity не совпадает с ожидаемым'
            assert response.json()['status'] == payload['status'], 'status заказа не совпадает с ожидаемым'
            assert response.json()['complete'] == payload['complete'], 'Комплектация заказа не совпадает с ожидаемой'

    @allure.title("Получение информации о заказе по ID")
    def test_get_order_by_id(self,create_an_order):
        with allure.step('Получение ID заказа'):
            order_id = create_an_order['id']
        with allure.step('Отправка запроса на получение информации о заказе'):
            response = requests.get(url = f'{BASE_URL}/store/order/{order_id}')
        with allure.step('Проверка статуса ответа и данных о заказе'):
            assert response.status_code == 200 , 'Код ответа не совпадает с ожидаемым'
            assert response.json()['id'] == order_id, 'ID заказа не совпадает с ожидаемым'

    @allure.title("Удаление заказа по ID")
    def test_deleted_order_by_id(self,create_an_order):
        with allure.step('Получение ID заказа'):
            order_id = create_an_order['id']
        with allure.step('Отправка запроса на удаление заказа'):
            response = requests.delete(url = f'{BASE_URL}/store/order/{order_id}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200 , 'Код ответа не совпал с ожидаемым'
        with allure.step('Отправка запроса на получение информации по удаленному заказу'):
            response = requests.get(url = f'{BASE_URL}/store/order/{order_id}')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404 , 'Код ответа не совпал с ожидаемым'

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step('Отправка запроса на получение информации о заказе'):
            response = requests.get(url = f'{BASE_URL}/store/order/9999')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 404 , 'Код ответа не совпал с ожидаемым'
        with allure.step('Проверка текстового содержимого ответа'):
            assert response.text == 'Order not found' , 'Текст ошибки не совпал с ожидаемым'

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory_petshop(self):
        with allure.step('Отправка запроса на получение инвентаря магазина'):
            response = requests.get(url = f'{BASE_URL}/store/inventory')
        with allure.step('Проверка статуса ответа'):
            assert response.status_code == 200 , 'Код ответа не совпадает с ожидаемым'
            jsonschema.validate(response.json(), INVENTORY_PETSHOP_SCHEMA) , 'Формат данных не совпал с ожидаемым'





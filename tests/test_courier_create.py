import pytest
import requests
from const import BASE_URL
from helpers import generate_courier_data


@pytest.fixture()
def delete_courier():
    # словарь, куда тест положит данные созданного курьера
    created = {}
    yield created
    # после теста: если курьер создан — логинимся и удаляем его
    if created:
        login_payload = {"login": created["login"], "password": created["password"]}
        login_response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=login_payload)
        courier_id = login_response.json().get("id")
        if courier_id:
            requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')


class TestCreateCourier:

    def test_create_courier_success(self, delete_courier):
        payload = generate_courier_data()
        delete_courier["login"] = payload["login"]
        delete_courier["password"] = payload["password"]

        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    def test_create_duplicate_courier_error(self, delete_courier):
        payload = generate_courier_data()
        delete_courier["login"] = payload["login"]
        delete_courier["password"] = payload["password"]

        # первый запрос — курьер создаётся
        requests.post(f'{BASE_URL}/api/v1/courier', data=payload)
        # второй с тем же логином — ошибка
        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        assert response.status_code == 409

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_error(self, missing_field):
        payload = generate_courier_data()
        payload.pop(missing_field)

        response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

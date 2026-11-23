import pytest
import methods
from helpers import generate_courier_data


@pytest.fixture()
def create_and_delete_courier():
    # создаём курьера, отдаём тесту данные и результат ответа,
    # после теста удаляем курьера
    payload = generate_courier_data()
    response = methods.create_courier(payload)
    data = {
        "payload": payload,
        "status_code": response.status_code,
        "body": response.json(),
    }
    yield data
    if data["status_code"] == 201:
        login_response = methods.login_courier(payload["login"], payload["password"])
        courier_id = login_response.json().get("id")
        if courier_id:
            methods.delete_courier(courier_id)


@pytest.fixture()
def registered_courier():
    return methods.register_new_courier_and_return_login_password()

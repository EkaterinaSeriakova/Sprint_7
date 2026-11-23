import pytest
import methods
from helpers import generate_courier_data


class TestCreateCourier:

    def test_create_courier_success(self, create_and_delete_courier):
        assert create_and_delete_courier["status_code"] == 201
        assert create_and_delete_courier["body"] == {"ok": True}

    def test_create_duplicate_courier_error(self, create_and_delete_courier):
        payload = create_and_delete_courier["payload"]

        # второй запрос с тем же логином — ошибка
        response = methods.create_courier(payload)

        assert response.status_code == 409
        assert "Этот логин уже используется" in response.json()["message"]

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_create_courier_missing_field_error(self, missing_field):
        payload = generate_courier_data()
        payload.pop(missing_field)

        response = methods.create_courier(payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

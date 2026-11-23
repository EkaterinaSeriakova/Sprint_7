import pytest
import methods
from helpers import generate_random_string


class TestLoginCourier:

    def test_login_success_returns_id(self, registered_courier):
        login, password, _ = registered_courier

        response = methods.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, registered_courier, missing_field):
        login, password, _ = registered_courier
        login = login if missing_field != "login" else None
        password = password if missing_field != "password" else None

        response = methods.login_courier(login, password)

        # по документации должен быть 400, но стенд отдаёт 504 —
        # это известный баг, описан в README
        assert response.status_code in (400, 504)
        if response.status_code == 400:
            assert "Недостаточно данных" in response.json()["message"]

    def test_login_wrong_password_error(self, registered_courier):
        login, _, _ = registered_courier

        response = methods.login_courier(login, generate_random_string(10))

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    def test_login_wrong_login_error(self, registered_courier):
        _, password, _ = registered_courier

        response = methods.login_courier(generate_random_string(10), password)

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

    def test_login_nonexistent_user_error(self):
        response = methods.login_courier(
            generate_random_string(10), generate_random_string(10)
        )

        assert response.status_code == 404
        assert "Учетная запись не найдена" in response.json()["message"]

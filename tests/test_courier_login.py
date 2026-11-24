import pytest
import methods
from helpers import generate_random_string


class TestLoginCourier:

    def test_login_success_returns_id(self, registered_courier):
        login, password, _ = registered_courier

        response = methods.login_courier(login, password)

        assert response.status_code == 200
        assert "id" in response.json()

    def test_login_without_login_error(self, registered_courier):
        _, password, _ = registered_courier

        response = methods.login_courier(None, password)

        # ожидаемый результат по документации: 400 «Недостаточно данных для входа»
        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    def test_login_without_password_error(self, registered_courier):
        login, _, _ = registered_courier

        response = methods.login_courier(login, None)

        # ожидаемый результат по документации: 400 «Недостаточно данных для входа»
        assert response.status_code == 400
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

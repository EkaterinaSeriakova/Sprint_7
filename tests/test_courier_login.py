import pytest
import requests
from const import BASE_URL
from helpers import register_new_courier_and_return_login_password, generate_random_string


@pytest.fixture()
def registered_courier():
    return register_new_courier_and_return_login_password()


class TestLoginCourier:

    def test_login_success_returns_id(self, registered_courier):
        login, password, _ = registered_courier

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": password}
        )

        assert response.status_code == 200
        assert "id" in response.json()

    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_missing_field_error(self, registered_courier, missing_field):
        login, password, _ = registered_courier
        payload = {"login": login, "password": password}
        payload.pop(missing_field)

        response = requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)

        assert response.status_code == 400
        assert "Недостаточно данных" in response.json()["message"]

    def test_login_wrong_password_error(self, registered_courier):
        login, _, _ = registered_courier

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": login, "password": generate_random_string(10)}
        )

        assert response.status_code == 404

    def test_login_wrong_login_error(self, registered_courier):
        _, password, _ = registered_courier

        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": generate_random_string(10), "password": password}
        )

        assert response.status_code == 404

    def test_login_nonexistent_user_error(self):
        response = requests.post(
            f'{BASE_URL}/api/v1/courier/login',
            data={"login": generate_random_string(10), "password": generate_random_string(10)}
        )

        assert response.status_code == 404

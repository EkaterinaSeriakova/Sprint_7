import pytest
import requests
from const import BASE_URL


@pytest.mark.parametrize("color", [
    ["BLACK"],
    ["GREY"],
    ["BLACK", "GREY"],
    []
])
def test_create_order_with_colors(color):
    payload = {
        "firstName": "Тест",
        "lastName": "Тестов",
        "address": "ул. Пушкина, 1",
        "metroStation": 4,
        "phone": "+7 999 999 99 99",
        "rentTime": 5,
        "deliveryDate": "2026-11-25",
        "comment": "Без комментариев",
        "color": color
    }

    response = requests.post(f'{BASE_URL}/api/v1/orders', json=payload)

    assert response.status_code == 201
    assert "track" in response.json()

import requests
from const import BASE_URL


class TestOrdersList:

    def test_get_orders_list(self):
        response = requests.get(f'{BASE_URL}/api/v1/orders')

        assert response.status_code == 200
        body = response.json()
        assert "orders" in body
        assert isinstance(body["orders"], list)

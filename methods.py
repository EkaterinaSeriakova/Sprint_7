import requests
from const import BASE_URL
from helpers import generate_courier_data


def create_courier(payload):
    return requests.post(f'{BASE_URL}/api/v1/courier', data=payload)


def login_courier(login, password):
    payload = {}
    if login is not None:
        payload["login"] = login
    if password is not None:
        payload["password"] = password
    return requests.post(f'{BASE_URL}/api/v1/courier/login', data=payload)


def delete_courier(courier_id):
    return requests.delete(f'{BASE_URL}/api/v1/courier/{courier_id}')


def register_new_courier_and_return_login_password():
    payload = generate_courier_data()
    response = create_courier(payload)
    if response.status_code == 201:
        return [payload["login"], payload["password"], payload["firstName"]]
    return []

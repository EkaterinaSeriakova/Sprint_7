import requests
import random
import string
from const import BASE_URL


def generate_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_data():
    return {
        "login": generate_random_string(10),
        "password": generate_random_string(10),
        "firstName": generate_random_string(10),
    }


def register_new_courier_and_return_login_password():
    payload = generate_courier_data()

    response = requests.post(f'{BASE_URL}/api/v1/courier', data=payload)

    if response.status_code == 201:
        return [payload["login"], payload["password"], payload["firstName"]]

    return []

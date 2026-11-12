import re
from functools import lru_cache

import requests

BASE_URL = "https://pokeapi.co/api/v2"


@lru_cache(maxsize=128)  # Уже загруженные ответы используем повторно.
def get_json(url):
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 404:
            raise ValueError("Такой покемон не найден. Проверьте имя на английском.")
        response.raise_for_status()  # Проверяем, что сервер ответил без ошибки.
        return response.json()  # Превращаем JSON-ответ в словарь Python.
    except requests.RequestException as error:
        raise ValueError("Не удалось получить данные PokéAPI. Попробуйте позже.") from error


def get_first_pokemon():
    data = get_json(f"{BASE_URL}/pokemon?limit=20&offset=0")
    return [pokemon["name"] for pokemon in data["results"]]


def get_pokemon(name):
    name = name.strip().lower()
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("Введите имя покемона на английском, например pikachu.")
    data = get_json(f"{BASE_URL}/pokemon/{name}/")
    # Оставляем нужные поля, чтобы с ними было проще работать дальше.
    return {
        "name": data["name"],
        "types": ", ".join(item["type"]["name"] for item in data["types"]),
        "weight": data["weight"] / 10,  # В API вес в гектограммах, здесь в кг.
        "height": data["height"] / 10,  # В API рост в дециметрах, здесь в метрах.
        "abilities": ", ".join(item["ability"]["name"] for item in data["abilities"]),
        "image": data["sprites"]["front_default"],
        "stats": {item["stat"]["name"]: item["base_stat"] for item in data["stats"]},
    }

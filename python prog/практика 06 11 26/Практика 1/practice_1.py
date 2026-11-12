# Практика 1. Откройте терминал в этой папке и выполните:
# python -m pip install -r requirements.txt
# python practice_1.py

import re

import requests


API_URL = "https://pokeapi.co/api/v2/pokemon"


def get_json(url):
    response = requests.get(url, timeout=15)
    if response.status_code == 404:
        raise ValueError("Покемон не найден. Проверьте имя на английском.")
    response.raise_for_status()  # Если сервер вернул ошибку, переходим в except.
    return response.json()  # Получаем словарь Python из ответа API.


def main():
    try:
        data = get_json(f"{API_URL}?limit=20&offset=0")
        print("Первые 20 покемонов:")
        for number, pokemon in enumerate(data["results"], start=1):
            print(f"{number}. {pokemon['name']}")

        name = input("Имя покемона: ").strip().lower()
        if not re.fullmatch(r"[a-z0-9-]+", name):
            raise ValueError("Введите имя на английском, например clefairy.")

        pokemon = get_json(f"{API_URL}/{name}/")
        types = ", ".join(item["type"]["name"] for item in pokemon["types"])
        abilities = ", ".join(
            item["ability"]["name"] for item in pokemon["abilities"]
        )

        print(f"Имя: {pokemon['name']}")
        print(f"Тип: {types}")
        # API хранит вес в гектограммах, рост в дециметрах: делим на 10.
        print(f"Вес: {pokemon['weight'] / 10} кг")
        print(f"Рост: {pokemon['height'] / 10} м")
        print(f"Способности: {abilities}")
    except requests.RequestException:
        print("Не удалось получить данные PokéAPI. Проверьте интернет.")
    except ValueError as error:
        print(error)


if __name__ == "__main__":
    main()

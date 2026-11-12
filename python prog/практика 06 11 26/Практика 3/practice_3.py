# Практика 3. Откройте терминал в этой папке и выполните:
# python -m pip install -r requirements.txt
# python practice_3.py
# Команда хранится в памяти, пока программа запущена.

import re

import requests


API_URL = "https://pokeapi.co/api/v2/pokemon"
pokemon_cache = {}  # Повторно используем уже полученные ответы API.


def get_pokemon(name):
    name = name.strip().lower()
    if not re.fullmatch(r"[a-z0-9-]+", name):
        raise ValueError("Введите имя на английском, например pikachu.")
    if name in pokemon_cache:
        return pokemon_cache[name]

    try:
        response = requests.get(f"{API_URL}/{name}/", timeout=15)
        if response.status_code == 404:
            raise ValueError("Покемон не найден.")
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as error:
        raise ValueError("PokéAPI недоступен. Проверьте интернет.") from error

    # Из ответа API составляем небольшой словарь с нужными нам данными.
    pokemon = {
        "name": data["name"],
        "types": ", ".join(item["type"]["name"] for item in data["types"]),
        "weight": data["weight"] / 10,
        "height": data["height"] / 10,
        "abilities": ", ".join(item["ability"]["name"] for item in data["abilities"]),
        "stats": {item["stat"]["name"]: item["base_stat"] for item in data["stats"]},
    }
    pokemon_cache[name] = pokemon
    pokemon_cache[pokemon["name"]] = pokemon
    return pokemon


def show_pokemon(pokemon):
    print(f"\nИмя: {pokemon['name']}")
    print(f"Тип: {pokemon['types']}")
    print(f"Вес: {pokemon['weight']} кг")
    print(f"Рост: {pokemon['height']} м")
    print(f"Способности: {pokemon['abilities']}")
    labels = {
        "hp": "Здоровье", "attack": "Атака", "defense": "Защита",
        "special-attack": "Особая атака", "special-defense": "Особая защита",
        "speed": "Скорость",
    }
    for stat, value in pokemon["stats"].items():
        print(f"{labels.get(stat, stat)}: {value}")


def add_pokemon(team, name):
    pokemon = get_pokemon(name)
    if pokemon["name"] in team:
        print("Этот покемон уже есть в команде.")
    else:
        # Имя — ключ словаря: один и тот же покемон не появится дважды.
        team[pokemon["name"]] = pokemon
        print(f"{pokemon['name']} добавлен в команду.")


def remove_pokemon(team, name):
    name = name.strip().lower()
    if name in team:
        del team[name]
        print(f"{name} удалён из команды.")
    else:
        print("Такого покемона нет в команде.")


def training_battle(first, second):
    fighters = [first, second]
    health = [first["stats"]["hp"], second["stats"]["hp"]]
    # Более быстрый ходит первым; при равной скорости — первый выбранный.
    turn = 0 if first["stats"]["speed"] >= second["stats"]["speed"] else 1
    log = []
    while health[0] > 0 and health[1] > 0:
        enemy = 1 - turn
        # Правило учебного боя: атака минус половина защиты, минимум 1 урона.
        damage = max(1, fighters[turn]["stats"]["attack"] - fighters[enemy]["stats"]["defense"] // 2)
        health[enemy] = max(0, health[enemy] - damage)
        log.append(
            f"{fighters[turn]['name']} наносит {damage} урона. "
            f"У {fighters[enemy]['name']} осталось {health[enemy]} HP."
        )
        turn = enemy
    winner = first["name"] if health[0] > 0 else second["name"]
    # health — отдельный список: исходные характеристики команды не меняются.
    return winner, log


def battle(team, first_name, second_name):
    first_name = first_name.strip().lower()
    second_name = second_name.strip().lower()
    if first_name not in team or second_name not in team:
        print("Оба покемона должны быть в вашей команде.")
    elif first_name == second_name:
        print("Выберите двух разных покемонов.")
    else:
        winner, log = training_battle(team[first_name], team[second_name])
        for line in log:
            print(line)
        print(f"Победитель: {winner}")


def main():
    team = {}
    # После каждого действия снова показываем меню. 0 завершает программу.
    while True:
        print("\n1 — Найти покемона")
        print("2 — Добавить покемона в команду")
        print("3 — Показать всю команду с подробностями")
        print("4 — Удалить покемона из команды")
        print("5 — Тренировочный бой")
        print("0 — Выход")
        choice = input("Выберите действие: ").strip()
        try:
            if choice == "1":
                show_pokemon(get_pokemon(input("Имя покемона: ")))
            elif choice == "2":
                add_pokemon(team, input("Имя покемона: "))
            elif choice == "3":
                if not team:
                    print("Команда пока пустая.")
                for pokemon in team.values():
                    show_pokemon(pokemon)
            elif choice == "4":
                remove_pokemon(team, input("Имя покемона для удаления: "))
            elif choice == "5":
                if len(team) < 2:
                    print("Сначала добавьте хотя бы двух покемонов.")
                    continue
                print("В команде:", ", ".join(team))
                first = input("Первый участник: ")
                second = input("Второй участник: ")
                battle(team, first, second)
            elif choice == "0":
                print("Программа завершена.")
                break
            else:
                print("Введите номер пункта меню.")
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()

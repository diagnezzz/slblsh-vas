from pokemon_api import get_first_pokemon, get_pokemon


def main():
    try:
        print("Первые 20 покемонов:")
        for number, name in enumerate(get_first_pokemon(), start=1):
            print(f"{number}. {name}")

        name = input("Имя покемона: ")
        pokemon = get_pokemon(name)
        print(f"Имя: {pokemon['name']}")
        print(f"Тип: {pokemon['types']}")
        print(f"Вес: {pokemon['weight']} кг")
        print(f"Рост: {pokemon['height']} м")
        print(f"Способности: {pokemon['abilities']}")
    except ValueError as error:
        print(error)


if __name__ == "__main__":  # Запускаем программу, только если открыли именно этот файл.
    main()

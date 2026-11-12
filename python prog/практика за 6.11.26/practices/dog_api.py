import requests


def dog_request(path):
    try:
        response = requests.get(f"https://dog.ceo/api/{path}", timeout=15)
        response.raise_for_status()
        data = response.json()
        if data["status"] != "success":
            raise ValueError("Dog API не смог выполнить запрос.")
        return data["message"]
    except requests.RequestException as error:
        raise ValueError("Dog API недоступен. Попробуйте позже.") from error


def get_breeds():
    breeds = dog_request("breeds/list/all")
    # Номера начинаются с 1. В шаблоне выведем номер и название каждой породы.
    return list(enumerate(sorted(breeds), start=1))


def get_dog_images(names, available_breeds):
    images = []
    errors = []
    for name in names:
        if name not in available_breeds:
            errors.append(f"Порода «{name}» не найдена в списке.")
            continue
        try:
            url = dog_request(f"breed/{name}/images/random")
            images.append({"breed": name, "url": url})
        except ValueError as error:
            errors.append(f"{name}: {error}")
    return images, errors

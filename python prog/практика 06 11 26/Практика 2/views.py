import requests
from django.shortcuts import render
from django.views.decorators.http import require_GET


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
    # Получаем пары: (1, название породы), (2, название породы) и так далее.
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


@require_GET
def dogs(request):
    # GET содержит данные, которые пользователь отправил через форму.
    text = request.GET.get("breeds", "")
    breeds, images, errors = [], [], []
    try:
        breeds = get_breeds()
        if "breeds" in request.GET:
            names = []
            for part in text.split(","):
                name = part.strip().lower()
                if name and name not in names:
                    names.append(name)
            if not names:
                errors.append("Введите хотя бы одну породу.")
            else:
                images, errors = get_dog_images(
                    names, [name for number, name in breeds]
                )
    except ValueError as error:
        errors.append(str(error))

    # Передаём данные в HTML: шаблон покажет список пород и фотографии.
    return render(request, "dogs.html", {
        "text": text, "breeds": breeds, "images": images, "errors": errors,
    })

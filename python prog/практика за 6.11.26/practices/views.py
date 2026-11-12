from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from pokemon_api import get_pokemon
from .battle import training_battle
from .dog_api import get_breeds, get_dog_images


@require_GET
def dogs(request):
    # Получаем текст, который пользователь ввёл в форму на странице.
    text = request.GET.get("breeds", "")
    breeds, images, errors = [], [], []
    try:
        breeds = get_breeds()
        if "breeds" in request.GET:
            # Разбиваем строку по запятым, убираем пробелы и повторы.
            names = list(dict.fromkeys(name.strip().lower() for name in text.split(",") if name.strip()))
            if not names:
                errors.append("Введите хотя бы одну породу.")
            else:
                images, errors = get_dog_images(names, [name for number, name in breeds])
    except ValueError as error:
        errors.append(str(error))
    # render подставляет данные из словаря в HTML-шаблон.
    return render(request, "practices/dogs.html", {
        "breeds": breeds, "images": images, "errors": errors, "text": text,
    })


@require_GET
def team(request):
    name = request.GET.get("name", "")
    found, error = None, None
    if "name" in request.GET:
        try:
            found = get_pokemon(name)
        except ValueError as problem:
            error = str(problem)
    return render(request, "practices/team.html", {
        "team": request.session.get("team", []),
        "found": found, "error": error, "name": name,
        "battle": request.session.pop("battle", None),
    })


@require_POST
def add_pokemon(request):
    team = request.session.get("team", [])
    try:
        pokemon = get_pokemon(request.POST.get("name", ""))
        if any(member["name"] == pokemon["name"] for member in team):
            messages.info(request, "Этот покемон уже в команде.")
        else:
            team.append(pokemon)
            # Сессия сохраняет отдельную команду для каждого браузера.
            request.session["team"] = team
            messages.success(request, f"{pokemon['name']} добавлен в команду.")
    except ValueError as error:
        messages.error(request, str(error))
    return redirect("team")


@require_POST
def remove_pokemon(request):
    name = request.POST.get("name", "")
    # Оставляем в команде всех покемонов, кроме выбранного для удаления.
    request.session["team"] = [
        pokemon for pokemon in request.session.get("team", []) if pokemon["name"] != name
    ]
    return redirect("team")


@require_POST
def battle(request):
    # Делаем словарь, чтобы находить участника команды по его имени.
    team = {pokemon["name"]: pokemon for pokemon in request.session.get("team", [])}
    first = request.POST.get("first")
    second = request.POST.get("second")
    if first not in team or second not in team:
        messages.error(request, "Выберите двух покемонов из своей команды.")
    elif first == second:
        messages.error(request, "Для боя нужны два разных покемона.")
    else:
        request.session["battle"] = training_battle(team[first], team[second])
    return redirect("team")

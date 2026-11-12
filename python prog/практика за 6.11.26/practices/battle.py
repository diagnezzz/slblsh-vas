def training_battle(first, second):
    # Здоровье храним отдельно: тренировка не меняет покемонов в команде.
    fighters = [first, second]
    health = [first["stats"]["hp"], second["stats"]["hp"]]
    # Более быстрый ходит первым; при равной скорости первым ходит first.
    turn = 0 if first["stats"]["speed"] >= second["stats"]["speed"] else 1
    log = []
    while health[0] > 0 and health[1] > 0:
        enemy = 1 - turn
        # Учебное правило боя: атака минус половина защиты, но минимум 1 урона.
        damage = max(1, fighters[turn]["stats"]["attack"] - fighters[enemy]["stats"]["defense"] // 2)
        health[enemy] = max(0, health[enemy] - damage)
        log.append(
            f"{fighters[turn]['name']} наносит {damage} урона. "
            f"У {fighters[enemy]['name']} осталось {health[enemy]} HP."
        )
        turn = enemy
    winner = first["name"] if health[0] > 0 else second["name"]
    return {"winner": winner, "log": log}

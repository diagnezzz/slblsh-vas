from datetime import date, datetime, timedelta
from decimal import Decimal


# Формат даты: год-месяц-день.
DATE_FORMAT = '%Y-%m-%d'

# Здесь будут храниться продукты и их партии.
goods = {}


def add(items, title, amount, expiration_date=None):
    # Если срок годности указан, преобразуем строку в дату.
    if expiration_date is not None:
        expiration_date = datetime.strptime(
            expiration_date, DATE_FORMAT
        ).date()

    # Для нового продукта создаём пустой список партий.
    if title not in items:
        items[title] = []

    # Добавляем партию с количеством и сроком годности.
    items[title].append({
        'amount': Decimal(str(amount)),
        'expiration_date': expiration_date
    })


def add_by_note(items, note):
    # Разбиваем запись на отдельные слова.
    parts = note.split()
    expiration_date = None

    # Проверяем, похожа ли последняя часть на дату ГГГГ-ММ-ДД.
    if len(parts[-1]) == 10 and parts[-1][4] == '-' and parts[-1][7] == '-':
        # Забираем дату и удаляем её из списка.
        expiration_date = parts.pop()

    # После удаления даты последняя часть — количество продукта.
    amount = Decimal(parts.pop())

    # Оставшиеся слова составляют название продукта.
    title = ' '.join(parts)

    # Добавляем продукт через готовую функцию.
    add(items, title, amount, expiration_date)


def find(items, needle):
    result = []

    # Ищем совпадения в названиях без учёта регистра.
    for title in items:
        if needle.lower() in title.lower():
            result.append(title)

    return result


def get_amount(items, needle):
    total = Decimal('0')

    # Находим подходящие продукты и складываем количество во всех партиях.
    for title in find(items, needle):
        for batch in items[title]:
            total += batch['amount']

    return total


def get_expired(items, in_advance_days=0):
    # Определяем дату, на которую проверяем срок годности.
    target_date = date.today() + timedelta(days=in_advance_days)
    result = []

    for title in items:
        # Для каждого продукта считаем количество отдельно.
        total = Decimal('0')

        for batch in items[title]:
            expiration_date = batch['expiration_date']

            # Партии без срока годности пропускаем.
            if expiration_date is not None:
                # Учитываем партии со сроком до выбранной даты включительно.
                if expiration_date <= target_date:
                    total += batch['amount']

        # Добавляем название и количество просроченного продукта.
        if total > 0:
            result.append((title, total))

    return result

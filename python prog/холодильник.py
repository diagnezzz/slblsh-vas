from datetime import date, datetime, timedelta
from decimal import Decimal


DATE_FORMAT = '%Y-%m-%d'

goods = {}


def add(items, title, amount, expiration_date=None):
    if expiration_date is not None:
        expiration_date = datetime.strptime(
            expiration_date, DATE_FORMAT
        ).date()

    if title not in items:
        items[title] = []

    items[title].append({
        'amount': Decimal(str(amount)),
        'expiration_date': expiration_date
    })


def add_by_note(items, note):
    parts = note.split()
    expiration_date = None

    if len(parts[-1]) == 10 and parts[-1][4] == '-' and parts[-1][7] == '-':
        expiration_date = parts.pop()

    amount = Decimal(parts.pop())
    title = ' '.join(parts)

    add(items, title, amount, expiration_date)


def find(items, needle):
    result = []
    for title in items:
        if needle.lower() in title.lower():
            result.append(title)
    return result


def get_amount(items, needle):
    total = Decimal('0')

    for title in find(items, needle):
        for batch in items[title]:
            total += batch['amount']

    return total


def get_expired(items, in_advance_days=0):
    target_date = date.today() + timedelta(days=in_advance_days)
    result = []

    for title in items:
        total = Decimal('0')

        for batch in items[title]:
            expiration_date = batch['expiration_date']

            if expiration_date is not None:
                if expiration_date <= target_date:
                    total += batch['amount']

        if total > 0:
            result.append((title, total))

    return result

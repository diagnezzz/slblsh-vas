import random
import secrets
import string


# Практика. Калькулятор
def add_numbers(a: float, b: float) -> float:
    """Возвращает сумму a и b."""
    return a + b


def divide(a: float, b: float) -> float:
    """Делит a на b; нулевой делитель запрещён."""
    if b == 0:
        raise ValueError("На ноль делить нельзя.")
    return a / b


def numpy_demo():
    """Проверяет работу NumPy."""
    import numpy as np

    numbers = np.array([1, 2, 3, 4, 5])
    total = np.sum(numbers)
    if total != 15:
        raise AssertionError("Неверный результат вычисления суммы.")
    print("NumPy:", np.__version__)
    print("Массив:", numbers)
    print("Сумма:", total)


def division_demo():
    """Проверяет деление и обработку нуля."""
    print("10 / 2 =", divide(10, 2))
    try:
        print(divide(10, 0))
    except ValueError as error:
        print(error)


def test_add_numbers():
    """Проверяет функцию сложения."""
    assert add_numbers(2, 3) == 5
    assert add_numbers(-5, 2) == -3
    assert add_numbers(0, 0) == 0
    assert abs(add_numbers(0.1, 0.2) - 0.3) < 1e-9


# Задача 1. Шифр Цезаря
ENGLISH = string.ascii_lowercase


RUSSIAN = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"


def detect_language(text):
    """Определяет язык текста."""
    has_russian = any(letter in RUSSIAN for letter in text.lower())
    has_english = any(letter in ENGLISH for letter in text.lower())
    if has_russian and has_english:
        return "русский и английский"
    if has_russian:
        return "русский"
    if has_english:
        return "английский"
    return "русских и английских букв нет"


def caesar_cipher(text, shift, decrypt=False):
    """Сдвигает буквы; decrypt=True отменяет шифрование."""
    if decrypt:
        shift = -shift
    result = []
    for letter in text:
        lower = letter.lower()
        if lower in RUSSIAN:
            alphabet = RUSSIAN
        elif lower in ENGLISH:
            alphabet = ENGLISH
        else:
            result.append(letter)
            continue
        # Замыкаем алфавит в кольцо.
        index = (alphabet.index(lower) + shift) % len(alphabet)
        new_letter = alphabet[index]
        result.append(new_letter.upper() if letter.isupper() else new_letter)
    return "".join(result)


# Задача 2. Олимпиада
def check_winners(scores, student_score):
    """Печатает, входит ли Стас в тройку лучших."""
    if student_score in sorted(scores, reverse=True)[:3]:
        print("Вы в тройке победителей!")
    else:
        print("Вы не попали в тройку победителей.")


# Задача 3. Пироженки и коробочки
def print_pack_report(number):
    """Выводит варианты фасовки от number до 1."""
    if type(number) is not int or number <= 1:
        raise ValueError("Нужно целое число больше единицы.")
    for count in range(number, 0, -1):
        if count % 3 == 0 and count % 5 == 0:
            message = "расфасуем по 3 или по 5"
        elif count % 5 == 0:
            message = "расфасуем по 5"
        elif count % 3 == 0:
            message = "расфасуем по 3"
        else:
            message = "не заказываем!"
        print(f"{count} - {message}")


# Задача 4. Пароли
def ask_yes_no(prompt):
    """Считывает ответ да или нет."""
    while True:
        answer = input(f"{prompt} [д/н]: ").strip().lower()
        if answer in ("д", "да", "y", "yes"):
            return True
        if answer in ("н", "нет", "n", "no"):
            return False
        print("Ответьте д или н.")


def generate_password(
    length, lowercase=True, uppercase=True, special=True, digits=True
):
    """Создаёт пароль с выбранными группами символов."""
    groups = []
    for enabled, characters in (
        (lowercase, string.ascii_lowercase),
        (uppercase, string.ascii_uppercase),
        (special, string.punctuation),
        (digits, string.digits),
    ):
        if enabled:
            groups.append(characters)
    if not groups:
        raise ValueError("Выберите хотя бы одну группу символов.")
    if type(length) is not int or length < len(groups):
        raise ValueError(f"Минимальная длина: {len(groups)}.")
    password = [secrets.choice(group) for group in groups]
    alphabet = "".join(groups)
    for _ in range(length - len(password)):
        password.append(secrets.choice(alphabet))
    secrets.SystemRandom().shuffle(password)
    return "".join(password)


# Задача 5. Римский конвертер
ROMAN_VALUES = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)


def to_roman(number):
    """Переводит число от 1 до 3999 в римскую запись."""
    if type(number) is not int or not 1 <= number <= 3999:
        raise ValueError("Введите целое число от 1 до 3999.")
    result = []
    for value, symbol in ROMAN_VALUES:
        while number >= value:
            result.append(symbol)
            number -= value
    return "".join(result)


def from_roman(text):
    """Переводит римское число в обычное."""
    text = text.strip().upper()
    values = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    if not text or any(letter not in values for letter in text):
        raise ValueError("Допустимы только римские цифры IVXLCDM.")
    result = 0
    previous = 0
    for letter in reversed(text):
        value = values[letter]
        if value < previous:
            result -= value
        else:
            result += value
        previous = value
    # Отсекаем записи вроде IIII и VX.
    if not 1 <= result <= 3999 or to_roman(result) != text:
        raise ValueError("Неверная римская запись числа от 1 до 3999.")
    return result


# Задача 6. Виселица
WORDS = ("программа", "функция", "переменная", "алгоритм", "компьютер")


HANGMAN = (
    " +---+\n |   |\n     |\n     |\n     |\n=====",
    " +---+\n |   |\n O   |\n     |\n     |\n=====",
    " +---+\n |   |\n O   |\n |   |\n     |\n=====",
    " +---+\n |   |\n O   |\n/|   |\n     |\n=====",
    " +---+\n |   |\n O   |\n/|\\  |\n     |\n=====",
    " +---+\n |   |\n O   |\n/|\\  |\n/    |\n=====",
    " +---+\n |   |\n O   |\n/|\\  |\n/ \\  |\n=====",
)


def play_hangman(word=None):
    """Запускает виселицу с шестью допустимыми ошибками."""
    if word is None:
        word = random.choice(WORDS)
    word = word.lower()
    if not word or any(letter not in RUSSIAN for letter in word):
        raise ValueError("Слово должно состоять из русских букв.")
    guessed = set()
    mistakes = 0
    print("Угадайте слово. Можно ошибиться 6 раз. Буквы е и ё различаются.")
    while True:
        print(HANGMAN[mistakes])
        print("Слово:", " ".join(c if c in guessed else "_" for c in word))
        print("Названные буквы:", " ".join(sorted(guessed)) or "нет")
        if all(letter in guessed for letter in word):
            print("Победа! Загаданное слово:", word)
            return True
        if mistakes == 6:
            print("Вы проиграли. Загаданное слово:", word)
            return False
        letter = input("Введите одну русскую букву: ").strip().lower()
        if len(letter) != 1 or letter not in RUSSIAN:
            print("Нужна одна русская буква.")
            continue
        if letter in guessed:
            print("Эта буква уже была. Попытка не тратится.")
            continue
        guessed.add(letter)
        if letter not in word:
            mistakes += 1




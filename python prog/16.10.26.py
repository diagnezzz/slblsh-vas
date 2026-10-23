from abc import ABC, abstractmethod
from datetime import date
import random


# Задания 1-4. Книги
# Дочерние классы обязаны реализовать print_info().
class Printable(ABC):
    @abstractmethod
    def print_info(self):
        pass


class Book(Printable):
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def info(self):
        return f"{self.title}, {self.author}, {self.year} г."

    # Представление книги при вызове print().
    def __str__(self):
        return self.info()

    # Сравниваем данные книг, а не сами объекты.
    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (self.title, self.author, self.year) == (
            other.title,
            other.author,
            other.year,
        )

    # Возраст вычисляется по текущему году.
    @property
    def age(self):
        return date.today().year - self.year

    # При изменении возраста пересчитываем год издания.
    @age.setter
    def age(self, value):
        if type(value) is not int or not 0 <= value < date.today().year:
            raise ValueError("Возраст должен быть целым и неотрицательным.")
        self.year = date.today().year - value

    # Формат строки: название;автор;год.
    @classmethod
    def from_string(cls, data):
        title, author, year = data.split(";")
        return cls(title.strip(), author.strip(), int(year))

    def print_info(self):
        print(self.info())


class Ebook(Book):
    def __init__(self, title, author, year, format="PDF"):
        # Основные поля книги задаёт родительский класс.
        super().__init__(title, author, year)
        self.format = format

    def info(self):
        return f"{super().info()}, формат: {self.format}"


def books_example():
    book = Book("1984", "Джордж Оруэлл", 1949)
    ebook = Ebook("Дюна", "Фрэнк Герберт", 1965, "EPUB")
    print(book.info())
    print(ebook.info())
    print(book)
    same_book = Book.from_string("1984;Джордж Оруэлл;1949")
    print("Книги равны:", book == same_book)
    print("Возраст книги:", book.age)
    same_book.age = 10
    print("Год после изменения возраста:", same_book.year)
    book.print_info()
    ebook.print_info()


# Практика 1. Сотрудники
class Employee:
    def __init__(self, name, base_salary):
        if base_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary


class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        if bonus < 0:
            raise ValueError("Премия не может быть отрицательной.")
        self.bonus = bonus

    def calculate_salary(self):
        # Зарплата менеджера: оклад и премия.
        return self.base_salary + self.bonus


class Developer(Employee):
    def __init__(self, name, base_salary, overtime_hours, hourly_rate):
        super().__init__(name, base_salary)
        if overtime_hours < 0 or hourly_rate < 0:
            raise ValueError("Часы и ставка не могут быть отрицательными.")
        self.overtime_hours = overtime_hours
        self.hourly_rate = hourly_rate

    def calculate_salary(self):
        # Дополнительные часы оплачиваются по часовой ставке.
        return self.base_salary + self.overtime_hours * self.hourly_rate


def employees_example():
    employees = [
        Employee("Иван", 50000),
        Manager("Анна", 70000, 15000),
        Developer("Олег", 90000, 10, 1500),
    ]
    for employee in employees:
        print(f"{employee.name}: {employee.calculate_salary()} руб.")


# Практика 2. Транспорт
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def description(self):
        return f"Транспорт: {self.brand}"


class Car(Vehicle):
    def __init__(self, brand, seats):
        super().__init__(brand)
        self.seats = seats

    def description(self):
        return f"Автомобиль {self.brand}, мест: {self.seats}"


class Bicycle(Vehicle):
    def __init__(self, brand, gears):
        super().__init__(brand)
        self.gears = gears

    def description(self):
        return f"Велосипед {self.brand}, передач: {self.gears}"


class Bus(Vehicle):
    def __init__(self, brand, route):
        super().__init__(brand)
        self.route = route

    def description(self):
        return f"Автобус {self.brand}, маршрут: {self.route}"


def vehicles_example():
    vehicles = [Car("Лада", 5), Bicycle("Stels", 7), Bus("ЛиАЗ", 12)]
    # Один метод вызывает разные реализации у разных классов.
    for vehicle in vehicles:
        print(vehicle.description())


# Практика 3. Онлайн-магазин
class Product:
    def __init__(self, name, price, stock, category):
        if price < 0 or type(stock) is not int or stock < 0:
            raise ValueError("Неверная цена или остаток товара.")
        self.name = name
        self.price = price
        self.stock = stock
        self.category = category

    def is_available(self, quantity):
        return type(quantity) is int and 0 < quantity <= self.stock


class ShoppingCart:
    def __init__(self):
        # Ключ — товар, значение — его количество в корзине.
        self.items = {}

    def add_product(self, product, quantity=1):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Количество должно быть целым и положительным.")
        total = self.items.get(product, 0) + quantity
        if not product.is_available(total):
            raise ValueError("На складе недостаточно товара.")
        self.items[product] = total

    def remove_product(self, product):
        self.items.pop(product, None)

    def update_quantity(self, product, quantity):
        if product not in self.items:
            raise ValueError("Товара нет в корзине.")
        if not product.is_available(quantity):
            raise ValueError("Недопустимое количество товара.")
        self.items[product] = quantity

    def total_price(self):
        return round(sum(p.price * q for p, q in self.items.items()), 2)


class Customer:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.orders = []

    def update_info(self, name, email):
        self.name = name
        self.email = email

    def order_history(self):
        # Копия защищает сам список истории от изменений снаружи.
        return self.orders.copy()


class Order:
    def __init__(self, customer, cart, discount=0, tax=0):
        if not 0 <= discount <= 100 or not 0 <= tax <= 100:
            raise ValueError(
                "Скидка и налог задаются в процентах от 0 до 100."
            )
        if not cart.items:
            raise ValueError("Корзина пуста.")
        self.customer = customer
        self.cart = cart
        self.discount = discount
        self.tax = tax
        # Фиксируем цену и количество на момент создания заказа.
        self.items = [(p, p.name, p.price, q) for p, q in cart.items.items()]
        self.status = "создан"

    def total_price(self):
        subtotal = sum(
            price * quantity for _, _, price, quantity in self.items
        )
        # Сначала применяем скидку, затем начисляем налог.
        discounted = subtotal * (1 - self.discount / 100)
        return round(discounted * (1 + self.tax / 100), 2)

    def checkout(self):
        if self.status != "создан":
            raise ValueError("Заказ уже оформлен.")
        if self.cart.items != {p: q for p, _, _, q in self.items}:
            raise ValueError("Корзина изменена. Создайте новый заказ.")
        # Сначала проверяем весь заказ, затем списываем остатки.
        for product, _, _, quantity in self.items:
            if not product.is_available(quantity):
                raise ValueError(f"Недостаточно товара: {product.name}")
        for product, _, _, quantity in self.items:
            product.stock -= quantity
        self.status = "оформлен"
        self.customer.orders.append(self)
        self.cart.items.clear()
        return self.total_price()


def shop_example():
    customer = Customer("Савелий", "saveliy@example.com")
    notebook = Product("Тетрадь", 100, 20, "Канцелярия")
    pen = Product("Ручка", 50, 30, "Канцелярия")
    cart = ShoppingCart()
    cart.add_product(notebook, 2)
    cart.add_product(pen, 3)
    cart.update_quantity(notebook, 4)
    cart.remove_product(pen)
    cart.add_product(pen)
    print("Стоимость корзины:", cart.total_price())
    order = Order(customer, cart, discount=10, tax=20)
    print("Стоимость со скидкой 10% и налогом 20%:", order.checkout())
    print("Осталось тетрадей:", notebook.stock)
    for item in customer.order_history():
        print("Заказ:", item.status, item.total_price(), "руб.")


# Практика 4. Космический корабль
class CrewMember:
    def __init__(self, name, role, skills):
        self.name = name
        self.role = role
        self.skills = list(skills)
        self.health = 100

    def take_damage(self, damage):
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным.")
        self.health = max(0, self.health - damage)

    def heal(self, amount):
        if amount < 0:
            raise ValueError("Лечение не может быть отрицательным.")
        self.health = min(100, self.health + amount)

    def learn_skill(self, skill):
        if skill not in self.skills:
            self.skills.append(skill)


class SpaceShip:
    def __init__(self, name, fuel):
        if fuel < 0:
            raise ValueError("Топливо не может быть отрицательным.")
        self.name = name
        self.fuel = fuel
        self.hull = 100
        self.speed = 0
        self.crew = []

    def add_crew(self, member):
        if member not in self.crew:
            self.crew.append(member)

    def refuel(self, amount):
        if amount < 0:
            raise ValueError("Количество топлива не может быть отрицательным.")
        self.fuel += amount

    def set_speed(self, speed):
        if speed < 0 or self.hull == 0:
            raise ValueError("Нельзя установить такую скорость.")
        self.speed = speed

    def fly(self, distance):
        if distance <= 0 or self.speed <= 0 or self.hull == 0:
            raise ValueError("Корабль не готов к полёту.")
        # Расход: 0.1 единицы топлива на единицу расстояния.
        required_fuel = distance * 0.1
        if self.fuel < required_fuel:
            raise ValueError("Недостаточно топлива.")
        self.fuel -= required_fuel
        return distance / self.speed

    def take_damage(self, damage):
        if damage < 0:
            raise ValueError("Урон не может быть отрицательным.")
        self.hull = max(0, self.hull - damage)
        if self.hull == 0:
            self.speed = 0

    def repair(self, engineer, amount):
        if amount <= 0 or self.hull == 0:
            raise ValueError("Ремонт невозможен.")
        if (
            engineer not in self.crew
            or engineer.role != "инженер"
            or engineer.health == 0
            or "ремонт" not in engineer.skills
        ):
            raise ValueError("Нужен здоровый инженер с навыком ремонта.")
        self.hull = min(100, self.hull + amount)


class Mission:
    def __init__(self, goal, distance, fuel_reserve, repair_kits):
        if distance <= 0 or fuel_reserve < 0:
            raise ValueError("Неверная дистанция или запас топлива.")
        if type(repair_kits) is not int or repair_kits < 0:
            raise ValueError("Неверное количество ремонтных комплектов.")
        self.goal = goal
        self.distance = distance
        self.resources = {"fuel": fuel_reserve, "repair_kits": repair_kits}
        self.events = ["авария", "астероиды", "спокойный полёт"]
        self.status = "запланирована"

    def handle_event(self, ship, event):
        if event not in self.events:
            raise ValueError("Неизвестное событие.")
        print("Событие:", event)
        if event == "авария":
            ship.take_damage(30)
            for member in ship.crew:
                member.take_damage(10)
        elif event == "астероиды":
            ship.take_damage(20)
        # Для ремонта нужны инженер и ремонтный комплект.
        if 0 < ship.hull < 100 and self.resources["repair_kits"] > 0:
            for member in ship.crew:
                if (
                    member.role == "инженер"
                    and member.health > 0
                    and "ремонт" in member.skills
                ):
                    ship.repair(member, 25)
                    self.resources["repair_kits"] -= 1
                    print("Инженер отремонтировал корпус.")
                    break

    def start(self, ship, event=None):
        if self.status != "запланирована":
            raise ValueError("Миссия уже запускалась.")
        if event is not None and event not in self.events:
            raise ValueError("Неизвестное событие.")
        pilots = [m for m in ship.crew if m.role == "пилот" and m.health > 0]
        if not pilots or ship.hull == 0:
            raise ValueError("Нужны пилот и исправный корабль.")
        if ship.fuel + self.resources["fuel"] < self.distance * 0.1:
            raise ValueError("Топлива не хватит на миссию.")
        # Переносим резерв миссии в бак корабля.
        ship.refuel(self.resources["fuel"])
        self.resources["fuel"] = 0
        ship.set_speed(100)
        self.status = "выполняется"
        # Если событие не задано, выбираем его случайно.
        self.handle_event(
            ship, event if event is not None else random.choice(self.events)
        )
        if ship.hull == 0 or not any(m.health > 0 for m in pilots):
            self.status = "провалена"
            ship.speed = 0
            return
        hours = ship.fly(self.distance)
        ship.set_speed(0)
        self.status = "завершена"
        print(f"Цель: {self.goal}. Время полёта: {hours} ч.")


def space_example():
    ship = SpaceShip("Восток", 50)
    pilot = CrewMember("Алексей", "пилот", ["управление"])
    engineer = CrewMember("Мария", "инженер", ["ремонт"])
    ship.add_crew(pilot)
    ship.add_crew(engineer)
    mission = Mission("Доставить груз на станцию", 500, 20, 1)
    mission.start(ship, event="астероиды")
    print("Статус миссии:", mission.status)
    print("Топливо:", ship.fuel, "Корпус:", ship.hull, "Скорость:", ship.speed)
    for member in ship.crew:
        print(member.name, member.role, "Здоровье:", member.health)


if __name__ == "__main__":
    print("Задания 1-4. Книги")
    books_example()
    print("\nПрактика 1. Сотрудники")
    employees_example()
    print("\nПрактика 2. Транспорт")
    vehicles_example()
    print("\nПрактика 3. Онлайн-магазин")
    shop_example()
    print("\nПрактика 4. Космический корабль")
    space_example()

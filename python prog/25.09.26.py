#task_1
temperature_C = int(input("Введите температуру в градусах Цельсия: "))
temperature_F = (temperature_C * 9/5) + 32
temperature_K = temperature_C + 273.15

print("Температура в Фаренгейтах: ", temperature_F)
print("Температура в Кельвинах: ", temperature_K)


#task_2
n = int(input("Введите число: "))

if n % 2 == 0:
    print(n, "- четное число")
else:
    print(n, "- нечетное число")
if n > 0:
    print(n, "- положительное число")
elif n < 0:
    print(n, "- отрицательное число")
else:
    print(n, "- ноль")
if 10 <= n <= 50:
    print(n, " находится в диапазоне от 10 до 50")

#task 3
import random

letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
x = "0123456789"
y = "!@#$%^&*"

password = []


for i in range(3):
    password.append(random.choice(letters))


for i in range(3):
    password.append(random.choice(x))


for i in range(2):
    password.append(random.choice(y))


random.shuffle(password)


result = "".join(password)

print("Твой пароль:", result)



#task 4
import collections
text=input("Введите текс: ").lower().replace(" ",'')
result = collections.Counter(text).most_common(3)
print("Три наиболее часто встречающиеся буквы:", result)

#task 5
def f(N):
    list_numbers = [True] * (N + 1)
    list_numbers[0] = list_numbers[1] = False
    for i in range(2, int(N**0.5) + 1):
        if list_numbers[i]:
            for j in range(i*i, N + 1, i):
                list_numbers[j] = False
    primes = [x for x in range(N + 1) if list_numbers[x]]
    return primes
print(f(1337))


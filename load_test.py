import random
import csv
from locust import HttpUser, task, between

# Загружаем данные из CSV-файла
users = []
with open('users_data.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        # Разделяем имя и фамилию
        full_name = row[0].split(' ')
        if len(full_name) == 2:
            last_name = full_name[0]
            first_name = full_name[1]
            users.append((last_name, first_name))

# Проверяем, сколько пользователей загружено
print(f"Загружено пользователей: {len(users)}")


class UserLoadTest(HttpUser):
    wait_time = between(1, 5)

    @task  # Помечаем метод как задачу для Locust
    def search_user(self):
        # Выбираем случайного пользователя из списка
        last_name, first_name = random.choice(users)

        # Берем первую букву имени и фамилии (префиксы)
        first_name_prefix = first_name[0]
        last_name_prefix = last_name[0]

        # Логируем информацию о пользователе, по которому ищем
        print(
            f"Ищем пользователя с фамилией, начинающейся с: {last_name_prefix}%, и именем, начинающимся с: {first_name_prefix}%")

        # Создаем и отправляем запрос с выбранными префиксами
        response = self.client.get(f"/users/search?first_name={first_name_prefix}&last_name={last_name_prefix}")

        # Логируем статус ответа
        print(f"Статус ответа: {response.status_code}, Ищем: {last_name_prefix}% {first_name_prefix}%")

        # Если запрос завершился с ошибкой, выводим детали
        if response.status_code != 200:
            print(f"Ошибка: {response.text}")

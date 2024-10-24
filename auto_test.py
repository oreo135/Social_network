import os
import subprocess
import time

# Определяем уровни нагрузки
concurrency_levels = [10, 100, 1000]

# Папка для сохранения результатов
results_folder = "test_results_with_hash_index"
os.makedirs(results_folder, exist_ok=True)

# Удаление всех старых файлов перед запуском тестирования
for filename in os.listdir(results_folder):
    file_path = os.path.join(results_folder, filename)
    try:
        if os.path.isfile(file_path):
            os.unlink(file_path)  # Удаляем файл
            print(f"Удален файл: {file_path}")
    except Exception as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")

# Запуск тестирования для каждого уровня нагрузки
for users in concurrency_levels:
    print(f"Запускаем тест для {users} пользователей...")

    # Имя файла для сохранения результатов
    result_file_prefix = os.path.join(results_folder, f"locust_{users}_users")

    # Запуск Locust с нужным количеством пользователей
    # --headless: запускаем в фоновом режиме без веб-интерфейса
    # --csv: сохраняем результаты в CSV с префиксом
    # --run-time: тестируем в течение 1 минуты для каждого уровня нагрузки
    command = [
        "locust",
        "-f", "load_test.py",
        "--headless",  # Запуск без веб-интерфейса
        "--users", str(users),  # Количество пользователей
        "--spawn-rate", "10",  # Скорость создания пользователей
        "--run-time", "1m",  # Время тестирования (1 минута)
        "--csv", result_file_prefix,  # Сохраняем результаты в CSV с префиксом
        "--host", "http://localhost:8000"  # URL вашего сервера
    ]

    # Запуск команды
    subprocess.run(command)

    print(f"Тест для {users} пользователей завершен. Результаты сохранены с префиксом {result_file_prefix}")

    # Ждем немного перед запуском следующего теста, чтобы сервер не перегружался
    time.sleep(5)

import os
import pandas as pd
import matplotlib.pyplot as plt

# Папка с результатами (без индексов)
results_folder = "test_results"

# Папка для сохранения графиков
output_folder = "gr_image_for_fulltext_index"
os.makedirs(output_folder, exist_ok=True)

# Уровни нагрузки
concurrency_levels = [10, 100, 1000]

latency_data = []
throughput_data = []

# Чтение данных для каждого уровня нагрузки
for users in concurrency_levels:
    stats_file = f"{results_folder}/locust_{users}_users_stats.csv"

    # Чтение файла с результатами
    data = pd.read_csv(stats_file)

    # Извлекаем среднее время отклика и пропускную способность
    avg_latency = data['Average Response Time'].mean()  # Средняя задержка
    avg_throughput = data['Requests/s'].mean()  # Пропускная способность (запросов в секунду)

    latency_data.append(avg_latency)
    throughput_data.append(avg_throughput)

# Построение графика Latency (задержка)
plt.figure()
plt.plot(concurrency_levels, latency_data, marker='o')
plt.title('Среднее время отклика (Latency) индекс fulltext')
plt.xlabel('Количество пользователей')
plt.ylabel('Latency (ms)')
plt.grid(True)
# Сохраняем график Latency в папку
plt.savefig(os.path.join(output_folder, "latency_with_index.png"))

# Построение графика Throughput (пропускная способность)
plt.figure()
plt.plot(concurrency_levels, throughput_data, marker='o')
plt.title('Пропускная способность (Throughput) индекс fulltext')
plt.xlabel('Количество пользователей')
plt.ylabel('Запросов в секунду (Requests/s)')
plt.grid(True)
# Сохраняем график Throughput в папку
plt.savefig(os.path.join(output_folder, "throughput_with_index.png"))

print(f"Графики сохранены в папке {output_folder}")

import pandas as pd
import matplotlib.pyplot as plt

# Загрузите данные из CSV-файла
df = pd.read_csv('locust_stats.csv')

# Фильтруем данные, чтобы использовать только конкретные запросы, а не агрегированные данные
filtered_df = df[df['Type'] == 'GET']

# Проверим наличие данных
print("Количество записей в данных:", len(filtered_df))
print("Первые строки данных:", filtered_df.head())

# Постройте график времени отклика и пропускной способности
plt.figure(figsize=(12, 8))

# График времени отклика
plt.subplot(2, 1, 1)
plt.plot(filtered_df['Request Count'], filtered_df['Median Response Time'], label='Median Response Time', color='blue')
plt.plot(filtered_df['Request Count'], filtered_df['Average Response Time'], label='Average Response Time', color='green')
plt.plot(filtered_df['Request Count'], filtered_df['Min Response Time'], label='Min Response Time', linestyle='--', color='purple')
plt.plot(filtered_df['Request Count'], filtered_df['Max Response Time'], label='Max Response Time', linestyle='--', color='red')
plt.xlabel('Number of Requests')
plt.ylabel('Response Time (ms)')
plt.title('Response Time Metrics')
plt.legend()
plt.grid()

# График пропускной способности
plt.subplot(2, 1, 2)
plt.plot(filtered_df['Request Count'], filtered_df['Requests/s'], label='Requests per Second', color='orange')
plt.plot(filtered_df['Request Count'], filtered_df['Failures/s'], label='Failures per Second', color='red')
plt.xlabel('Number of Requests')
plt.ylabel('Requests and Failures per Second')
plt.title('Throughput and Failures')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()

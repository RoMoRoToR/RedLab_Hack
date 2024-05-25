# src/main.py

import os
from utils import load_data, preprocess_data, compute_features, detect_anomalies, save_data, format_anomalies
from notification import notify_anomalies

if __name__ == "__main__":
    raw_data_path = "../data/example_data.tsv"
    processed_data_path = "../data/processed/processed_data.tsv"

    # Шаг 1: Загрузка и предобработка данных
    data = load_data(raw_data_path)
    processed_data = preprocess_data(data)

    # Шаг 2: Вычисление метрик
    features_data = compute_features(processed_data)

    # Шаг 3: Обнаружение аномалий
    anomalies_data = detect_anomalies(features_data, ['web_response', 'throughput', 'apdex', 'error_rate'])

    # Шаг 4: Сохранение данных
    save_data(anomalies_data, processed_data_path)

    # Шаг 5: Форматирование аномалий и отправка уведомлений
    anomalies = format_anomalies(anomalies_data)
    notify_anomalies(anomalies)

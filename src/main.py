# src/main.py

import sys
sys.path.append("..")

import pandas as pd
from src.data_processing import load_data, preprocess_data, save_data
from src.feature_engineering import compute_features
from src.anomaly_detection import detect_anomalies
from src.notification import notify_anomalies
from src.utils import format_anomalies

if __name__ == "__main__":
    raw_data_path = "../data/metrics_collector.tsv"
    processed_data_path = "../data/processed_data.tsv"
    features_data_path = "../data/features_data.tsv"
    anomalies_data_path = "../data/anomalies_data.tsv"

    # Шаг 1: Загрузка и предобработка данных
    data = load_data(raw_data_path)
    processed_data = preprocess_data(data)
    save_data(processed_data, processed_data_path)

    # Шаг 2: Вычисление метрик
    data_with_features = compute_features(processed_data)
    data_with_features.to_csv(features_data_path, sep='\t', index=False)

    # Шаг 3: Обнаружение аномалий
    features = ['web_response', 'throughput', 'apdex', 'error_rate']
    data_with_anomalies = detect_anomalies(data_with_features, features)
    data_with_anomalies.to_csv(anomalies_data_path, sep='\t', index=False)

    # Шаг 4: Форматирование аномалий и отправка уведомлений
    anomalies = format_anomalies(data_with_anomalies)
    notify_anomalies(anomalies)

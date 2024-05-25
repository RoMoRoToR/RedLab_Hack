# src/main.py

import sys
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Добавление пути к src в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

    logging.info("Starting the data processing pipeline...")

    # Проверка существования обработанных данных
    if not os.path.exists(processed_data_path):
        logging.info("Loading and preprocessing raw data...")
        data = load_data(raw_data_path)
        processed_data = preprocess_data(data)
        save_data(processed_data, processed_data_path)
    else:
        logging.info("Loading preprocessed data...")
        processed_data = pd.read_csv(processed_data_path, sep='\t')

    # Проверка существования данных с признаками
    if not os.path.exists(features_data_path):
        logging.info("Computing features...")
        data_with_features = compute_features(processed_data)
        data_with_features.to_csv(features_data_path, sep='\t', index=False)
    else:
        logging.info("Loading data with features...")
        data_with_features = pd.read_csv(features_data_path, sep='\t')

    logging.info("Detecting anomalies...")
    features = ['web_response', 'throughput', 'apdex', 'error_rate']
    data_with_anomalies = detect_anomalies(data_with_features, features)
    data_with_anomalies.to_csv(anomalies_data_path, sep='\t', index=False)

    logging.info("Formatting and sending anomaly notifications...")
    anomalies = format_anomalies(data_with_anomalies)
    notify_anomalies(anomalies)

    logging.info("Data processing pipeline completed successfully.")

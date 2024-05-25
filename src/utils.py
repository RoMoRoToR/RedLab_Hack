# src/utils.py

import pandas as pd
from datetime import timedelta

def load_data(filepath):
    """
    Загружает данные из TSV файла.
    """
    return pd.read_csv(filepath, sep='\t')

def preprocess_data(df):
    """
    Предобработка данных: обработка пропущенных значений, преобразование типов.
    """
    df['point'] = pd.to_datetime(df['point'])
    df = df.sort_values(by='point')
    df = df.fillna(0)  # Заполнение пропущенных значений нулями, можно улучшить метод
    return df

def compute_features(df):
    """
    Вычисляет ключевые метрики.
    """
    df['web_response'] = df['total_call_time'] / df['call_count']
    df['throughput'] = df['call_count']
    s = df['call_count']
    t = df['total_call_time']
    f = df['total_exclusive_time']
    df['apdex'] = (s + t / 2) / (s + t + f)
    df['error_rate'] = df.apply(lambda row: row['call_count'] if row['name'] == 'Errors/allWeb' else 0, axis=1) / df['call_count']
    return df

def detect_anomalies(df, features):
    """
    Выявляет аномалии в данных с использованием Isolation Forest.
    """
    from sklearn.ensemble import IsolationForest
    model = IsolationForest(contamination=0.01)
    df['anomaly'] = model.fit_predict(df[features])
    df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
    return df

def save_data(df, filepath):
    """
    Сохраняет предобработанные данные в указанный файл.
    """
    df.to_csv(filepath, sep='\t', index=False)

def format_anomalies(df):
    """
    Форматирует найденные аномалии для уведомления.
    """
    anomalies = df[df['anomaly'] == 1]
    formatted_anomalies = ""
    for _, row in anomalies.iterrows():
        formatted_anomalies += f"{row['point']}: Anomaly detected in {row['name']}\n"
    return formatted_anomalies

if __name__ == "__main__":
    # Пример использования утилит
    raw_data_path = "../data/example_data.tsv"
    processed_data_path = "../data/processed/processed_data.tsv"

    data = load_data(raw_data_path)
    processed_data = preprocess_data(data)
    features_data = compute_features(processed_data)
    anomalies_data = detect_anomalies(features_data, ['web_response', 'throughput', 'apdex', 'error_rate'])
    save_data(anomalies_data, processed_data_path)
    anomalies = format_anomalies(anomalies_data)
    print(anomalies)

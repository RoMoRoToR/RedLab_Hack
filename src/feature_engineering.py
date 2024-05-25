# src/feature_engineering.py

import pandas as pd

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

if __name__ == "__main__":
    processed_data_path = "../data/processed_data.tsv"
    features_data_path = "../data/features_data.tsv"

    data = pd.read_csv(processed_data_path, sep='\t')
    data_with_features = compute_features(data)
    data_with_features.to_csv(features_data_path, sep='\t', index=False)

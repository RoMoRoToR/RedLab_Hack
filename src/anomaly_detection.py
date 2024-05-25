# src/anomaly_detection.py

import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, features):
    """
    Выявляет аномалии в данных с использованием Isolation Forest.
    """
    model = IsolationForest(contamination=0.01)
    df['anomaly'] = model.fit_predict(df[features])
    df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
    return df

if __name__ == "__main__":
    features_data_path = "../data/features_data.tsv"
    anomalies_data_path = "../data/anomalies_data.tsv"

    data = pd.read_csv(features_data_path, sep='\t')
    features = ['web_response', 'throughput', 'apdex', 'error_rate']
    data_with_anomalies = detect_anomalies(data, features)
    data_with_anomalies.to_csv(anomalies_data_path, sep='\t', index=False)

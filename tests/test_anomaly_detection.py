# tests/test_anomaly_detection.py

import pandas as pd
from src.anomaly_detection import detect_anomalies

def test_detect_anomalies():
    data_path = '../data/processed/features_data.tsv'
    df = pd.read_csv(data_path, sep='\t')

    features = ['web_response', 'throughput', 'apdex', 'error_rate']
    df = detect_anomalies(df, features)
    assert 'anomaly' in df.columns

if __name__ == "__main__":
    test_detect_anomalies()

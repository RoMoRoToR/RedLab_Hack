# src/utils.py

import pandas as pd

def format_anomalies(df):
    """
    Форматирует найденные аномалии для уведомления.
    """
    anomalies = df[df['anomaly'] == 1]
    formatted_anomalies = ""
    for _, row in anomalies.iterrows():
        formatted_anomalies += f"{row['point']}: Anomaly detected in {row['name']}\n"
    return formatted_anomalies

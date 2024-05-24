# src/feature_engineering.py

import pandas as pd

def compute_web_response(df):
    """
    Вычисляет время ответа сервиса.
    """
    df['web_response'] = df['total_call_time'] / df['call_count']
    return df

def compute_throughput(df):
    """
    Вычисляет пропускную способность сервиса.
    """
    df['throughput'] = df['call_count']
    return df

def compute_apdex(df):
    """
    Вычисляет APDEX.
    """
    s = df['call_count']
    t = df['total_call_time']
    f = df['total_exclusive_time']
    df['apdex'] = (s + t / 2) / (s + t + f)
    return df

def compute_error_rate(df):
    """
    Вычисляет процент ошибок в обработанных запросах.
    """
    df['error_rate'] = df.apply(lambda row: row['call_count'] if row['name'] == 'Errors/allWeb' else 0, axis=1) / df['call_count']
    return df

if __name__ == "__main__":
    data_path = '../data/processed/processed_data.tsv'
    df = pd.read_csv(data_path, sep='\t')

    df = compute_web_response(df)
    df = compute_throughput(df)
    df = compute_apdex(df)
    df = compute_error_rate(df)

    df.to_csv('../data/processed/features_data.tsv', sep='\t', index=False)

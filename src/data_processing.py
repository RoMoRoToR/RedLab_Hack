import pandas as pd
import os

def load_data(filepath):
    data = pd.read_csv(filepath, sep='\t', header=None)
    columns = [
        'account_id', 'name', 'timestamp', 'call_count', 'total_call_time', 'total_exclusive_time',
        'min_call_time', 'max_call_time', 'sum_of_squares', 'instances', 'language', 'app_name',
        'app_id', 'scope', 'host', 'display_host', 'pid', 'agent_version', 'labels'
    ]
    data.columns = columns
    return data

def preprocess_data(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values(by='timestamp')
    df = df.fillna(0)
    return df

def save_data(df, filepath):
    df.to_csv(filepath, sep='\t', index=False)

if __name__ == "__main__":
    data_path = "../data/metrics_collector.tsv"
    processed_data_path = "../data/processed_data.tsv"

    data = load_data(data_path)
    processed_data = preprocess_data(data)
    save_data(processed_data, processed_data_path)

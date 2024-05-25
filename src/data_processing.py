# src/data_processing.py

import pandas as pd
import os


def load_data(filepath):
    """
    Загружает данные из TSV файла без заголовков и устанавливает имена столбцов.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    data = pd.read_csv(filepath, sep='\t', header=None)
    columns = [
        'account_id', 'name', 'point', 'call_count', 'total_call_time', 'total_exclusive_time',
        'min_call_time', 'max_call_time', 'sum_of_squares', 'instances', 'language', 'app_name',
        'app_id', 'scope', 'host', 'display_host', 'pid', 'agent_version', 'labels'
    ]
    data.columns = columns
    return data


def preprocess_data(df):
    """
    Предобработка данных: обработка пропущенных значений, преобразование типов.
    """
    df['point'] = pd.to_datetime(df['point'])
    df = df.sort_values(by='point')
    df = df.fillna(0)  # Заполнение пропущенных значений нулями
    return df


def save_data(df, filepath):
    """
    Сохраняет предобработанные данные в указанный файл.
    """
    df.to_csv(filepath, sep='\t', index=False)


if __name__ == "__main__":
    raw_data_path = "../data/metrics_collector.tsv"
    processed_data_path = "../data/processed_data.tsv"

    data = load_data(raw_data_path)
    processed_data = preprocess_data(data)
    save_data(processed_data, processed_data_path)

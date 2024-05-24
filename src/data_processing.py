import pandas as pd

def load_data(filepath):
    """
    Загружает данные из TSV файла.
    """
    return pd.read_csv(filepath, sep='data/metrics_collector.tsv')

def preprocess_data(df):
    """
    Предобработка данных: обработка пропущенных значений, преобразование типов.
    """
    df['point'] = pd.to_datetime(df['point'])
    df = df.sort_values(by='point')
    df = df.fillna(0)  # Заполнение пропущенных значений нулями, можно улучшить метод
    return df

def save_data(df, filepath):
    """
    Сохраняет предобработанные данные в указанный файл.
    """
    df.to_csv(filepath, sep='\t', index=False)

if __name__ == "__main__":
    raw_data_path = "../data/example_data.tsv"
    processed_data_path = "../data/processed/processed_data.tsv"

    data = load_data(raw_data_path)
    processed_data = preprocess_data(data)
    save_data(processed_data, processed_data_path)

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def detect_anomalies(df, feature):
    """
    Выявляет аномалии в данных с использованием LSTM.
    """
    # Нормализация данных
    scaler = MinMaxScaler()
    df[feature] = scaler.fit_transform(df[[feature]])

    # Создание последовательностей для LSTM
    def create_sequences(data, time_steps=10):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data.iloc[i:(i + time_steps)].values)
            y.append(data.iloc[i + time_steps)].values)
            return np.array(X), np.array(y)

        time_steps = 10
        X, y = create_sequences(df[feature], time_steps)

        # Определение и обучение модели LSTM
        model = Sequential()
        model.add(LSTM(units=64, return_sequences=True, input_shape=(time_steps, 1)))
        model.add(Dropout(0.2))
        model.add(LSTM(units=64, return_sequences=False))
        model.add(Dropout(0.2))
        model.add(Dense(units=1))

        model.compile(optimizer='adam', loss='mse')
        model.fit(X, y, epochs=10, batch_size=32)

        # Обнаружение аномалий
        predictions = model.predict(X)
        mse = np.mean(np.power(y - predictions, 2), axis=1)
        threshold = np.percentile(mse, 99)
        df['anomaly'] = 0
        df['anomaly'].iloc[time_steps:] = mse > threshold

        return df

    if __name__ == "__main__":
        features_data_path = "../data/metrics_collector.tsv"
        anomalies_data_path = "../data/anomalies_data.tsv"

        data = pd.read_csv(features_data_path, sep='\t')
        data['timestamp'] = pd.to_datetime(data['2024-04-15 23:32:00'], errors='coerce')
        data.set_index('timestamp', inplace=True)
        data = data.sort_index()
        feature = '0.1'

        data_with_anomalies = detect_anomalies(data, feature)
        data_with_anomalies.to_csv(anomalies_data_path, sep='\t', index=False)

import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df, features):

    model = IsolationForest(contamination=0.01)
    df['anomaly'] = model.fit_predict(df[features])
    df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
    return df

if __name__ == "__main__":
    data_path = '/data/processed/features_data.tsv'
    df = pd.read_csv(data_path, sep='\t')

    features = ['web_response', 'throughput', 'apdex', 'error_rate']
    df = detect_anomalies(df, features)

    df.to_csv('../data/processed/anomalies_data.tsv', sep='\t', index=False)

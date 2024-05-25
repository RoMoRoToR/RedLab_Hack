# tests/test_data_processing.py

import sys
sys.path.append("..")

import pandas as pd
from src.data_processing import load_data, preprocess_data

def test_load_data():
    filepath = '../data/metrics_collector.tsv'
    df = load_data(filepath)
    assert not df.empty

def test_preprocess_data():
    filepath = '../data/metrics_collector.tsv'
    df = load_data(filepath)
    processed_df = preprocess_data(df)
    assert processed_df.isnull().sum().sum() == 0

if __name__ == "__main__":
    test_load_data()
    test_preprocess_data()

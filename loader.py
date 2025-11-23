import os
import pandas as pd

def save_hourly_csv(df, path='data/hourly.csv'):
    os.makedirs(os.path.dirname(path), exist_ok= True)
    df.to_csv(path)
    return path

def save_hourly_parquet(df, path='data/hourly.parquet'):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_parquet(path)
    return path

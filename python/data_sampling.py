"""
NYC Yellow Taxi - Data Sampling
================================
Downloads the January 2024 NYC Yellow Taxi trip dataset (NYC TLC, ~38M+ rows)
and creates a reproducible 200,000-row sample for use in Tableau.

Run:
    python data_sampling.py

Output:
    taxi_sample.csv
"""

import pandas as pd

URL = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"
SAMPLE_SIZE = 200_000
RANDOM_STATE = 42


def main():
    print("Downloading NYC Yellow Taxi data (January 2024)...")
    df = pd.read_parquet(URL)
    print(f"Full dataset shape: {df.shape}")

    df_sample = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)
    print(f"Sampled shape: {df_sample.shape}")

    df_sample.to_csv("taxi_sample.csv", index=False)
    print("Saved sample to taxi_sample.csv")


if __name__ == "__main__":
    main()

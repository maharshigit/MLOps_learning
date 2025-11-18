import sys
import os
import pandas as pd
import pickle


import pyarrow as pa
import pyarrow.parquet as pq

def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)
S3_ENDPOINT_URL = "http://localhost:4566"

storage_options = {
    "client_kwargs": {"endpoint_url": S3_ENDPOINT_URL},
    "key": "test",
    "secret": "test"
}


def read_data(filename: str):
    """Read data from S3 or local path"""
    print("Reading:", filename)
    df = pd.read_parquet(filename, engine="fastparquet", storage_options=storage_options)
    print(df.head())
    return df


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    df = read_data(input_file)

    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    with open("model.bin", "rb") as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ["PULocationID", "DOLocationID"]
    dicts = df[categorical].to_dict(orient="records")
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print("Predicted mean duration:", y_pred.mean())

    df_result = pd.DataFrame()
    df_result["ride_id"] = df["ride_id"]
    df_result["predicted_duration"] = y_pred

    df_result.to_parquet(output_file, engine="pyarrow", index=False, storage_options=storage_options)
    print("Saved predictions to:", output_file)


if __name__ == "__main__":
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    os.environ["INPUT_FILE_PATTERN"] = "s3://nyc-duration/in/{year:04d}-{month:02d}.parquet"
    os.environ["OUTPUT_FILE_PATTERN"] = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"

    main(year, month)

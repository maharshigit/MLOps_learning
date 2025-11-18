#!/usr/bin/env python
# coding: utf-8

import boto3
import pandas as pd
import os
from datetime import datetime

S3_ENDPOINT_URL = "http://localhost:4566"
BUCKET_NAME = "nyc-duration"

options = {
    "client_kwargs": {"endpoint_url": S3_ENDPOINT_URL},
    "key": "test",
    "secret": "test"
}

# Sample dataframe similar to Q3/unit test
def create_sample_df():
    def dt(hour, minute, second=0):
        return datetime(2023, 1, 1, hour, minute, second)
    
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    return df

def main(year, month):
    df_input = create_sample_df()
    
    # Save to S3
    s3_output = f"s3://{BUCKET_NAME}/in/{year:04d}-{month:02d}.parquet"
    
    # Initialize S3 client
    s3 = boto3.resource(
        "s3",
        endpoint_url=S3_ENDPOINT_URL,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1",
    )
    
    # Create bucket if not exists
    if BUCKET_NAME not in [b.name for b in s3.buckets.all()]:
        s3.create_bucket(Bucket=BUCKET_NAME)
    
    df_input.to_parquet(
        s3_output,
        engine="pyarrow",
        compression=None,
        index=False,
        storage_options=options
    )
    
    print("Integration test parquet uploaded to:", s3_output)

if __name__ == "__main__":
    year = int(os.environ.get("YEAR", 2023))
    month = int(os.environ.get("MONTH", 1))
    main(year, month)

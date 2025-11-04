
#!/usr/bin/env python
# coding: utf-8



import boto3
import sys
import pickle
import pandas as pd
import boto3
import os 





categorical = ['PULocationID', 'DOLocationID']

def read_data(filename):
    
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df

S3_ENDPOINT_URL = "http://localhost:4566/"
options = {
    'client_kwargs': {
        'endpoint_url': S3_ENDPOINT_URL
    }
}



def get_input_path(year, month) -> str:
    """Get input path"""
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    """Get output path"""
    default_output_pattern = 's3://nyc-duration-prediction-alexey/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)



def main(year,month):
    
    input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'

    
    input_file = get_input_path(year, month)
    
    
    df = read_data(input_file)
    

    df.to_parquet(output_file, engine='pyarrow', index=False)
    output_file = get_output_path(year,month)
    print(output_file)
    df.to_parquet(
        output_file,
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    	)
    
    # s3 = boto3.resource('s3',S3_ENDPOINT_URL= S3_ENDPOINT_URL)

    # s3.Bucket("nyc-duration").upload_file(output_file, "dump/file")
    
    
    
if __name__=="__main__":
    os.environ['OUTPUT_FILE_PATTERN'] = "s3://nyc-duration/out/{year:04d}-{month:02d}.parquet"
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year,month)

        

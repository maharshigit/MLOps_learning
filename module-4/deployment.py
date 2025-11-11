
import pickle
import os
import pandas as pd

def read_model():
    with open('model/model.bin', 'rb') as f_in:
        dv, model = pickle.load(f_in)
    return model, dv



categorical = ['PULocationID', 'DOLocationID']

def read_data(filename,categorical):
    df = pd.read_parquet(filename)
    
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    
    return df
import sys 

year = sys.argv[1] 
month = sys.argv[2]

def predictions(categorical,year,month):
    model,dv = read_model()
    print("This are the input args ", year , month)
    print(categorical)
    data_location = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year}-0{month}.parquet'
    print(data_location)
    df = read_data(data_location,categorical)
    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = model.predict(X_val)

    # print(y_pred.std())
    print(y_pred.mean())





categorical = ['PULocationID', 'DOLocationID']
year = sys.argv[1] 
month = sys.argv[2]
predictions(categorical =categorical,year=year,month=month)

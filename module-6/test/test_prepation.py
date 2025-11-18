import pandas as pd
from datetime import datetime
from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),      # duration 9 min -> drop
        (1, 1, dt(1, 2), dt(1, 10)),            # duration 8 min -> keep
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),   # duration 59 min -> drop missing DO
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),       # duration > 60 min -> drop
    ]

    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)

    actual_df = prepare_data(df)

    expected_data = [
        (1, 1, dt(1, 2), dt(1, 10), 8.0)
    ]
    expected_columns = columns + ['duration']
    expected_df = pd.DataFrame(expected_data, columns=expected_columns)

    # Compare as list of dicts
    assert actual_df.to_dict(orient="records") == expected_df.to_dict(orient="records")

import pandas as pd
from etl.transformer import transform_openweather_hourly

def test_transform_openweather_hourly_empty():
    df = transform_openweather_hourly({'hourly': []})
    assert isinstance(df, pd.DataFrame)
    assert df.empty
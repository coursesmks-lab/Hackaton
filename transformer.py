import pandas as pd
def transform_openweather_hourly(onecall_json):
    """Convert onecall hourly list to DataFrame with datetime index."""
    if not onecall_json:
        return pd.DataFrame()
    hourly = onecall_json.get('hourly',[])
    if not hourly:
        return pd.DataFrame()
    df = pd.DataFrame(hourly)
    if 'dt' in df.columns:
        df['dt'] = pd.to_datetime(df['dt'],unit='s')
        df = df.set_index('dt')
    
    if 'weather' in df.columns:
        df['weather_main'] = df['weather'].apply(lambda v: v[0].get('main') if v else None)
        df['weather_desc'] = df['weather'].apply(lambda v: v[0].get('description') if v else None)
        df = df.drop(columns=['weather'])
    
    for c in df.columns:
        if df[c].dtype == 'object' and c not in ['weather_main','weather_desc']:
            try:
                df[c] = pd.to_numeric(df[c])
            except Exception:
                pass
    return df

def transform_current_current(current_json):
    """Return a small dict or DataFrame for current weather"""
    if not current_json:
        return None
    d = {
        'temp': current_json.get('main',{}).get('temp'),
        'feels_like':current_json.get('main',{}).get('feels_like'),
        'humidity': current_json.get('main',{}).get('humidity'),
        'wind_speed': current_json.get('wind',{}).get('speed'),
        'weather_main':current_json.get('weather',[{}])[0].get('main'),
        'weather_desc':current_json.get('weather',[{}])[0].get('description'),
        'dt':pd.to_datetime(current_json.get('dt',None), unit='s') if current_json.get('dt') else None
    }
    return d

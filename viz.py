import plotly.express as px
def plot_temperature(df, units = 'metric'):
    if df.empty:
        return None
    y_label = 'Temperature (C)' if units == 'metric' else 'Temperature (F)'
    fig = px.line(df.reset_index(), x='dt', y='temp', title=f'Temperature ({units})')
    fig.update_xaxes(title_text='Datetime')
    fig.update_yaxes(title_text = y_label)
    return fig

def plot_many_vars(df):
    if df.empty:
        return None
    return px.line(df.reset_index(), x='dt', y=['temp','humidity'], title= 'Temp & Humidity')
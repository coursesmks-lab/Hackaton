import streamlit as st
from datetime import datetime, timedelta
from api_client.openweather import OpenWeatherClient
from etl.extractor import extract_weather_by_city
from etl.transformer import transform_openweather_hourly, transform_current_current
from analysis.viz import plot_temperature, plot_many_vars
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(layout='wide', page_title='Weather ETL Dashboard')
st.title('Weather ETL & Visualization')

# Sidebar inputs
mode = st.sidebar.selectbox('Mode', ['Live', 'Cached Only'])
city = st.sidebar.text_input('City', 'Karachi')
units = st.sidebar.selectbox('Units', ['metric', 'imperial'])
refresh_minutes = st.sidebar.number_input('Auto-refresh (minutes)', min_value=1, max_value=60, value=5)
manual_refresh = st.sidebar.button('Refresh Now')
save_snapshots = st.sidebar.checkbox('Save snapshots to disk', value=False)

# Quantize time-based cache key
refresh_key = int((datetime.utcnow().timestamp()) // (refresh_minutes*60))

client = OpenWeatherClient()

cache_info = ''

st.sidebar.markdown('---')
st.sidebar.markdown('API & Cache info')
st.sidebar.write('Cache dir: `cache/`')

with st.spinner('Fetching data...'):
    try:
        payload = extract_weather_by_city(city, units=units)
        current = payload.get('current')
        onecall = payload.get('onecall')

        df_hourly = transform_openweather_hourly(onecall)
        current_small = transform_current_current(current)

        # show current
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader(f'Hourly forecast for {city}')
            if df_hourly.empty:
                st.info('No hourly data available.')
            else:
                # add dt as column for plotly clarity
                # df_hourly_plot = df_hourly.copy()
                # df_hourly_plot = df_hourly_plot.reset_index().rename(columns={'dt':'dt'})

                # df_hourly_plot = df_hourly.reset_index()
                # fig = plot_temperature(df_hourly_plot.rename(columns={'index':'dt'}), units=units)

                df_hourly_plot = df_hourly.reset_index()
                fig = plot_temperature(df_hourly_plot, units=units)

                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                # additional plot
                fig2 = plot_many_vars(df_hourly_plot)
                if fig2:
                    st.plotly_chart(fig2, use_container_width=True)
        with col2:
            st.subheader('Current')
            if current_small:
                st.write(current_small)
            else:
                st.info('No current data available.')

        # save snapshot if requested
        if save_snapshots and not df_hourly.empty:
            os.makedirs('snapshots', exist_ok=True)
            fname = f"snapshots/{city}_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.parquet"
            df_hourly.to_parquet(fname)
            st.success(f'Saved snapshot: {fname}')

        # show last-update info using cache metadata (best-effort)
        st.sidebar.success('Data fetched (may be from cache).')

    except Exception as e:
        st.error(str(e))
        # try to show cached info if any
        st.warning('If you previously loaded this city, cached data may still be available on disk in cache/.')
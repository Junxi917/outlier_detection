import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM


def forest_detection(df, contamination=0.05):
    model = IsolationForest(contamination=contamination)
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round('1min')
    df = df.sort_values('timestamp')

    col = df.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    new_df = df[col].copy()
    data = df[new_df.columns.values]

    scaler = StandardScaler()
    np_scaled = scaler.fit_transform(data)
    data = pd.DataFrame(np_scaled)
    model.fit(data)

    df['anomaly'] = pd.Series(model.fit_predict(data))

    outlier_data = df.loc[df['anomaly'] == -1]
    for index in outlier_data.index.tolist():
        df.loc[index, new_df.columns.values] = np.nan

    df = df[[sensor, 'timestamp']]
    return df


def gap_filling(df):
    col = df.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round('1min')
    df = df.sort_values('timestamp')

    start = pd.to_datetime(str(df['timestamp'].min()))
    end = pd.to_datetime(str(df['timestamp'].max()))

    df_date = df.set_index("timestamp")

    df_date = df_date.set_index(pd.to_datetime(df_date.index))

    pdates = pd.date_range(start=start, end=end, freq='5Min')

    df_date_new = df_date.reindex(pdates, fill_value=np.nan)

    df = df_date_new

    df = df.rename_axis('timestamp').reset_index()
    df = df[[sensor, 'timestamp']]

    df = df.interpolate(method='linear', limit_direction='forward')  # make a gap filling with interpolate

    return df

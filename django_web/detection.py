import pandas as pd
import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.svm import OneClassSVM
from pyod.models.hbos import HBOS
from pyod.models.cblof import CBLOF
from pyod.models.iforest import IForest
from pyod.models.pca import PCA
from pyod.models.lof import LOF


def forest_detection(df, algo_select, contamination=0.05):
    algo = {"Hbos": HBOS(contamination=contamination),
            "Forest": IForest(contamination=contamination),
            "Cblof": CBLOF(contamination=contamination),
            # "OCSVM": OCSVM(contamination=contamination),
            "Pca": PCA(contamination=contamination)}
    model = algo[algo_select]
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
    df['original'] = df[sensor]

    outlier_data = df.loc[df['anomaly'] == 1]
    for index in outlier_data.index.tolist():
        df.loc[index, new_df.columns.values] = np.nan

    df = df[[sensor, 'original', 'anomaly', 'timestamp']]
    return df


def gap_filling(df, filling_select):

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

    filling_data = df.loc[df[sensor].isnull()]

    # filling = {"Interpolate": df.interpolate(method='linear', limit_direction='forward'),
    #            "Mean": df.fillna(df[sensor].mean(), inplace=True),
    #            "Median": df.fillna(df[sensor].median(), inplace=True),
    #            }

    if filling_select == "Interpolate":
        df = df.interpolate(method='linear', limit_direction='forward')
    if filling_select == "Mean":
        df.fillna(df[sensor].mean(), inplace=True)
    if filling_select == "Median":
        df.fillna(df[sensor].median(), inplace=True)

    # df = df.interpolate(method='linear', limit_direction='forward')  # make a gap filling with interpolate

    df['filling'] = np.nan
    for index in filling_data.index.tolist():
        df.loc[index, 'filling'] = df.loc[index, sensor]

    return df

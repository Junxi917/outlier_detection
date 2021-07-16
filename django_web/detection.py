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

from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from tensorflow import keras


def forest_detection(df, algo_select, contamination=0.05):
    algo = {"Hbos": HBOS(contamination=contamination),
            "Forest": IForest(contamination=contamination),
            "Cblof": CBLOF(contamination=contamination), }
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
    if len(col) == 1:
        df['original'] = df[sensor]
    if len(col) == 2:
        df['original' + " " + col[0]] = df[col[0]]
        df['original' + " " + col[1]] = df[col[1]]

    outlier_data = df.loc[df['anomaly'] == 1]
    for index in outlier_data.index.tolist():
        df.loc[index, new_df.columns.values] = np.nan

    # df = df[[sensor, 'original', 'anomaly', 'timestamp']]
    return df


def gap_filling(df, filling_select):
    print (df.head())
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
    if len(col) == 1:
        df = df[[sensor, 'timestamp']]
    if len(col) == 2:
        df = df[[col[0], col[1], 'timestamp']]
    filling_data = df.loc[df[sensor].isnull()]

    # filling = {"Interpolate": df.interpolate(method='linear', limit_direction='forward'),
    #            "Mean": df.fillna(df[sensor].mean(), inplace=True),
    #            "Median": df.fillna(df[sensor].median(), inplace=True),
    #            }

    if filling_select == "Interpolate":
        # df = df.interpolate(method='linear', limit_direction='forward')
        df = df.interpolate(method='linear').ffill().bfill()
    if filling_select == "Mean":
        df.fillna(df[sensor].mean(), inplace=True)
    if filling_select == "Median":
        df.fillna(df[sensor].median(), inplace=True)

    # df = df.interpolate(method='linear', limit_direction='forward')  # make a gap filling with interpolate

    if len(col) == 1:
        sen = 'filling' + " " + col[0]
        df[sen] = np.nan
        for index in filling_data.index.tolist():
            df.at[index, sen] = df.at[index, sensor]
    if len(col) == 2:
        sen1 = 'filling' + " " + col[0]
        sen2 = 'filling' + " " + col[1]
        df[sen1] = np.nan
        df[sen2] = np.nan
        for index in filling_data.index.tolist():
            df.at[index, sen1] = df.at[index, col[0]]
            df.at[index, sen2] = df.at[index, col[1]]

    return df


TIME_STEPS = 30


def create_sequences(X, y, time_steps=TIME_STEPS):
    Xs, ys = [], []
    for i in range(len(X) - time_steps):
        Xs.append(X.iloc[i:(i + time_steps)].values)
        ys.append(y[i + time_steps])

    return np.array(Xs), np.array(ys)


train_model = {"KLT12_flowRate1 (l/min)": 'KLT12_flowRate1_model2.h5',
               "IT Power Consumption (W)": 'IT_Power_Consumption_model2.h5',
               "Outside Temperature (°C)": 'Outside_Temperature_model2.h5',
               "KLT11_pumpSpeed_p1 (Hz)": 'KLT11_pumpSpeed_p1_model2.h5',
               "KLT11_Fan1Speed_HZ (Hz)": 'KLT11_Fan1Speed_model2.h5',
               "KLT13_inletTempBeforeHydraulicGate": 'KLT13_inletTempBeforeHydraulicGate_model2.h5',
               "KLT11_inletTempBeforeHydraulicGate": 'KLT13_inletTempBeforeHydraulicGate_model2.h5',
               "KLT12_inletTempBeforeHydraulicGate": 'KLT13_inletTempBeforeHydraulicGate_model2.h5',
               "KLT14_inletTempBeforeHydraulicGate": 'KLT13_inletTempBeforeHydraulicGate_model2.h5',
               "KLT14_pumpSpeed_p1": 'multi_KLT14pumpSpeed_model1.h5',
               "KLT14_Fan1Speed_HZ": 'multi_KLT14_FanSpeed_model2.h5',
               }


def lstm_detection(df, contamination=0.05):
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round('1min')
    df = df.sort_values('timestamp')

    col = df.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    new_df = df[col].copy()

    model = load_model(train_model[sensor], compile=False)

    df_test = df

    test = df_test[[sensor]]
    test = test.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(test[[sensor]])

    test[sensor] = scaler.transform(test[[sensor]])

    testX, testY = create_sequences(test[[sensor]], test[sensor])

    predict = model.predict_on_batch(testX)

    test_mae_loss = np.mean(predict, axis=1)

    original_test = pd.DataFrame(test[sensor][30:])
    original_test = original_test.values

    test_mae_loss = np.abs(test_mae_loss - original_test)

    number_of_outliers = int(len(df) * contamination)
    data = np.array(test_mae_loss).reshape(len(test_mae_loss), 1)
    data_list = map(lambda x: x[0], data)
    test_mae_loss_df = pd.Series(data_list)

    threshold = test_mae_loss_df.nlargest(number_of_outliers).min()

    test_score_df = pd.DataFrame(df_test[TIME_STEPS:])

    test_score_df = test_score_df.reset_index()
    test_score_df = test_score_df[['timestamp', sensor]]
    test_score_df['anomaly'] = (test_mae_loss_df >= threshold).astype(int)

    test_score_df['original'] = test_score_df[sensor]

    outlier_data = test_score_df.loc[test_score_df['anomaly'] == 1]
    for index in outlier_data.index.tolist():
        test_score_df.loc[index, new_df.columns.values] = np.nan

    test_score_df = test_score_df[[sensor, 'original', 'anomaly', 'timestamp']]
    return test_score_df


train_multi_model = {"KLT14_pumpSpeed_p1 KLT14_pumpSpeed_p2": 'multi_KLT14pumpSpeed_model1.h5',
                     }


def multi_lstm_detection(df, contamination=0.05):
    df['timestamp'] = pd.to_datetime(df['timestamp']).dt.round('1min')
    df = df.sort_values('timestamp')

    col = df.columns.values.tolist()
    col.remove('timestamp')
    sensor = col[0]

    new_df = df[col].copy()

    model = load_model(train_multi_model[sensor + " " + col[1]], compile=False)

    df_test = df

    test = df_test[[col[0], col[1]]]
    test = test.astype('float32')
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(test[[sensor]])
    test[sensor] = scaler.transform(test[[sensor]])
    scaler = scaler.fit(test[[col[1]]])
    test[col[1]] = scaler.transform(test[[col[1]]])

    testX, testY = create_sequences(test[[col[0], col[1]]], test.values)

    predict = model.predict_on_batch(testX)

    test_mae_loss = np.mean(predict, axis=1)

    original_test = pd.DataFrame(test[col[1]][30:])
    original_test = original_test.values

    test_mae_loss = test_mae_loss[:, 1].reshape(len(testX), 1)
    test_mae_loss = np.abs(test_mae_loss - original_test)

    number_of_outliers = int(len(df) * contamination)
    data = np.array(test_mae_loss).reshape(len(test_mae_loss), 1)
    data_list = map(lambda x: x[0], data)
    test_mae_loss_df = pd.Series(data_list)

    threshold = test_mae_loss_df.nlargest(number_of_outliers).min()

    test_score_df = pd.DataFrame(df_test[TIME_STEPS:])

    test_score_df = test_score_df.reset_index()
    test_score_df = test_score_df[['timestamp', sensor, col[1]]]
    test_score_df['anomaly'] = (test_mae_loss_df >= threshold).astype(int)

    test_score_df['original' + " " + col[0]] = test_score_df[col[0]]
    test_score_df['original' + " " + col[1]] = test_score_df[col[1]]

    outlier_data = test_score_df.loc[test_score_df['anomaly'] == 1]
    for index in outlier_data.index.tolist():
        test_score_df.loc[index, new_df.columns.values] = np.nan

    test_score_df = test_score_df[
        [col[0], col[1], 'original' + " " + col[0], 'original' + " " + col[1], 'anomaly', 'timestamp']]
    return test_score_df

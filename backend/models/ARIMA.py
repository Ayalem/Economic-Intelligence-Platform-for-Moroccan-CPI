
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error as mse
from statsmodels.tsa.statespace.sarimax import SARIMAXResults


def model_ARIMA(df_finaly,train_until="2024-05-01"):
    train=df_finaly[:train_until]
    test=df_finaly[train_until:]
    model=SARIMAX(train,order=(1,1,0),seasonal_order=(1,1,1,12))
    model_fit=model.fit()
    return model_fit,test

def arima_forecast(model_fit,steps):
    forecast=model_fit.forecast(steps=steps)
    return forecast
def compute_metrics(model_fit,test):
    y_pred=arima_forecast(model_fit,steps=len(test))
    y_true=test
    y_true=y_true.values.ravel()
    MSE=mse(y_true,y_pred)
    RMSE=np.sqrt(MSE)
    MAPE=np.mean(np.abs(y_true-y_pred)/np.abs(y_true))*100
    metrics={"MSE":MSE,"RMSE":RMSE,"MAPE":MAPE}
    return metrics


#PLOT FORECAST
def arima_to_ploty_compare(forecast,df_finaly,train_until="2024-05-01"):
    df_compare=df_finaly[train_until:]
    df_compare.index=forecast.index

    lineplot=({
        "forecast":{
                 "x":forecast.index.strftime('%Y-%m-%d').tolist(),
                 "y":forecast.values.tolist()
        },
        "actual":{
                    "x":df_compare.index.strftime('%Y-%m-%d').tolist(),
                    "y":df_compare['IPC'].tolist()
        }
    })
    return lineplot
#plot compare
def arima_to_ploty_forecast(forecast,df_finaly,train_until="2024-05-01"):

    last_date=pd.to_datetime(df_finaly[train_until:].index[-1])
    last_val=df_finaly['IPC'].iloc[-1]
    forecast_after_test=forecast[forecast.index>last_date]
    future_index=pd.date_range(start=last_date+pd.DateOffset(months=1),periods=len(forecast_after_test),freq="MS")
    forecast_after_test.index=future_index
    forecast=pd.concat([pd.Series([last_val],index=[last_date]),forecast_after_test])

    lineplot=({
        "forecast":{
                 "x":forecast.index.strftime('%Y-%m-%d').tolist(),
                 "y":forecast.values.tolist()
        },
        "actual":{
                    "x":df_finaly.index.strftime('%Y-%m-%d').tolist(),
                    "y":df_finaly['IPC'].tolist()
        }
    })
    return lineplot
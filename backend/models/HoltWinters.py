import pandas as pd 
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error as mse
import matplotlib.pyplot as plt

def prepare_data(df_finaly,train_until="2024-05-01'"):
    train_holt_winter=df_finaly[:train_until]
    test_holt_winter=df_finaly[train_until:]
    model_holt_winter=ExponentialSmoothing(train_holt_winter,seasonal_periods=12,trend="mul",seasonal="add").fit(optimized=True)
    return model_holt_winter,test_holt_winter
def forecast(model,steps):
     forecast_holt_winter=model.forecast(steps)
     return forecast_holt_winter


def compute_metrics(model,test):
     y_pred=forecast(model,len(test))
     y_true=test
     y_true = y_true.values.ravel()  
     MSE=mse(y_pred,y_true)
     RMSE=np.sqrt(MSE)
     MAPE=np.mean(np.abs(y_true-y_pred)/np.abs(y_true))*100
     metrics={"MSE":MSE,"RMSE":RMSE,"MAPE":MAPE}
     return metrics
def winter_to_ploty_compare(forecast,df_finaly,train_until="2024-05-01"):
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

def winter_to_ploty_forecast(forecast,df_finaly,train_until="2024-05-01"):

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
def winter_to_ploty(forecast,df_finaly):
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


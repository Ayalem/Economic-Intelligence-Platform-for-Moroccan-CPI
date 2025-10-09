import numpy as np
import pandas as pd
from prophet import Prophet
from sklearn.metrics import mean_squared_error as mse
import json



def prepare_data(df_finaly,train_until="2024-05-01"):
         df_prophet=df_finaly.reset_index()
         df_prophet=df_prophet.rename(columns={'Date':'ds','IPC':'y'})
         train=df_prophet[df_prophet['ds']<train_until]
         test=df_prophet[df_prophet['ds']>=train_until]
         m=Prophet(yearly_seasonality=True, weekly_seasonality=False,
    daily_seasonality=False, changepoint_prior_scale=0.1, 
    changepoint_range=0.99)
         m.fit(train)
         return m,test




def compute_metrics(model,test):
    future=model.make_future_dataframe(periods=len(test),include_history=False,freq="MS")
    forecast=model.predict(future)
    merged_table=forecast[['ds','yhat']].merge(test,on='ds')
    y_true=merged_table['y']
    y_pred=merged_table['yhat']
    MSE=round(mse(y_pred,y_true),3)
    RMSE=np.sqrt(MSE)
    MAPE=np.mean(np.abs(y_pred-y_true)/np.abs(y_pred))*100
    metrics={"MSE":MSE,"RMSE":round(RMSE,3),"MAPE":round(MAPE,3)}
    return metrics

def predict_future(model,periods=365):
       future = model.make_future_dataframe(include_history=False,freq="MS",periods=periods)
       forecast=model.predict(future)
       return forecast

def ploty_forecast(actual,forecast):
       last_date=actual.index[-1]
       last_val=actual["IPC"].iloc[-1]
       extra_row=pd.DataFrame({"ds":[last_date],"yhat":[last_val], "yhat_lower": [last_val],
    "yhat_upper": [last_val]})
       forecast=forecast[forecast['ds']>last_date]
       forecast = pd.concat([extra_row, forecast[["ds","yhat","yhat_lower","yhat_upper"]]])

       lineplot={
              "actual": {
        "ds": actual.index.strftime('%Y-%m-%d').tolist(),
        "y": actual['IPC'].tolist()
    },
    "forecast": {
        "ds":forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "yhat": forecast['yhat'].tolist(),
        "yhat_lower": forecast['yhat_lower'].tolist(),
        "yhat_upper": forecast['yhat_upper'].tolist()
    }
}
       return lineplot
def ploty_compare(actual,forecast,train_until="2024-05-01"):
       actual=actual[train_until:]
       lineplot={
              "actual": {
        "ds": actual.index.strftime('%Y-%m-%d').tolist(),
        "y": actual['IPC'].tolist()
    },
    "forecast": {
        "ds":forecast['ds'].dt.strftime('%Y-%m-%d').tolist(),
        "yhat": forecast['yhat'].tolist(),
        "yhat_lower": forecast['yhat_lower'].tolist(),
        "yhat_upper": forecast['yhat_upper'].tolist()
    }
}
       return lineplot

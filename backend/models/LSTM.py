import pandas as pd 
import numpy as np
import tensorflow as tf
from models import prepare
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM
from sklearn.metrics import mean_squared_error as mse

def prepare_data(df_finaly,train_until="2024-05-01",seq_size=6,batch_size=1):
    train=df_finaly[:train_until]
    test=df_finaly[train_until:]
    scaler=StandardScaler()
    scaler.fit(train)
    train_scaled=scaler.transform(train).reshape(-1,1)
    test_scaled=scaler.transform(test).reshape(-1,1)
    train_generator=TimeseriesGenerator(train_scaled,train_scaled,length=seq_size,batch_size=batch_size)
    test_generator=TimeseriesGenerator(test_scaled,test_scaled,length=seq_size,batch_size=batch_size)
    return train_generator,test_generator,scaler




def evaluate_model(model,test_generator,scaler):
  print("evaluating model...")
  test_pred=model.predict(test_generator,verbose=1)
  print("Prediction:", test_pred)
  test_pred=scaler.inverse_transform(test_pred)
  print("inverse scaler:",test_pred)
  y_true=[]
  for i in range(len(test_generator)):
     print(f"loop{i}")
     _,y=test_generator[i]
     y_true.append(y)
     y_true =np.array(y_true).reshape(-1, 1)
     y_true=scaler.inverse_transform(y_true)
     metrics=compute_metrics(y_true,test_pred)
  return y_true,test_pred,metrics

def compute_metrics(y_true,test_pred):
    MSE=mse(y_true,test_pred)
    RMSE=np.sqrt(MSE)
    MAPE=np.mean(np.abs(y_true-test_pred)/np.abs(y_true))*100
    metrics={"MSE":MSE,"RMSE":RMSE,"MAPE":MAPE}
    return metrics

def concatenate_dates(df_finaly,test_pred):
    all_dates=df_finaly.loc["2024-10-01	":"2025-05-01"].index
    last_val=df_finaly.loc["2024-10-01"].values[0]
    y_pred=np.concatenate([[last_val], test_pred.flatten()])
    return all_dates,y_pred
############################################static version#############################################

def compute_metrics_static():
   df=pd.read_csv('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/models/df_metrics.csv')
   y_true,y_pred=df['y_true'],df['y_pred']
   MSE=mse(y_true,y_pred)
   RMSE=np.sqrt(MSE)
   MAPE=np.mean(np.abs(y_true-y_pred)/np.abs(y_true))*100
   metrics={"MSE":MSE,"RMSE":RMSE,"MAPE":MAPE}
   return metrics
def plot_compare():
   df=pd.read_csv('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/models/df_metrics.csv')
   lineplot={'actual':{
      'x':df.index.tolist(),
      'y':df['y_pred'].tolist()},
      'forecast':{
         "x":df.index.tolist(),
         "y":df['y_true'].tolist()
      }
      
      }
   return lineplot
def plot_forecast():
   df=pd.read_csv('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/models/df_forecast_12.csv')
   df_finaly=prepare.chainage()
   lineplot={
      'forecast':{
         "x":df['Date'].tolist(),
         "y":df['Forecast'].tolist()
      },
      "actual":{
          "x":df_finaly.index.strftime('%Y-%m-%d').tolist(),
          "y":df_finaly['IPC'].tolist()
      }
    }
   return lineplot


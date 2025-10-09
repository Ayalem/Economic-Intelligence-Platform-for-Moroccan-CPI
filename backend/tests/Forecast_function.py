import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error as mse
from statsmodels.tsa.statespace.sarimax import SARIMAXResults
from tensorflow.keras.model import load_models
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM

#2017 prepare
def preparing_2017(df):
  def verify_date(col):
    try:
        pd.to_datetime(col,format="%Y-%m-%d %H:%M:%S")
        return True
    except:
        return False
  city_map={
    1:'Agadir',
    2:'Casablanca',
    3:'Fes',
    4:'Kenitra',
    5:'Marrackech',
    6:'Oujda',
    7:'Rabat',
    8:'Tetouan',
    9:'Meknes',
    10:'Tanger',
    11:'Laayoune',
    12:'Dakhla',
    13:'Guelmim',
    14:'Settat',
    15:'Safi',
    16:'Beni Mellal',
    17:'Al-Houcima',
    18:'Errachidia',
    99:"National"
}
  date_cols=[col for col in df.columns  if verify_date(col)]
  df=df.melt(id_vars=["VILLE","coicop","libelle"],var_name="Date",value_vars=date_cols,value_name="IPC")
  df["VILLE"]=df["VILLE"].map(city_map)
  df["Date"]=pd.to_datetime(df["Date"],errors="coerce").astype(str)
  df=df[(df['VILLE']=="National")&(df['libelle']=='GENERAL')]
  df=df.drop(['VILLE','coicop','libelle'],axis=1)
  return df

def prepare_2006():
 excel_file = pd.ExcelFile('backend/IPC _2006_f.xlsx')
 sheet_names = excel_file.sheet_names

 data=pd.read_excel('backend/IPC _2006_f.xlsx',sheet_name=None)
 df=pd.DataFrame()
 df.head()
 for i in sheet_names:
      df_1=data[i]
      year=i[4:]
      new_col=[]
      df_1.columns = df_1.columns.str.strip().str.replace(' ', '') 
      for col in df_1.columns:
           
            if col not in ['VILLE','LIBELLE','code']:
                  new_col.append(f"{col}-{year}")
            else:
                  new_col.append(col)
      df_1.columns=new_col
 df=pd.DataFrame()
 for i in sheet_names:
    df_temp=data[i]
    df=pd.concat([df,df_temp],axis=1)
 df.head()
 month_map = {
    'janvier': '01',
    'février': '02',
    'mars': '03',
    'avril': '04',
    'mai': '05',
    'juin': '06',
    'juillet': '07',
    'août': '08',
    'septembre': '09',
    'octobre': '10',
    'novembre': '11',
    'décembre': '12'
}
 cols=[]
 for m in df.columns:
    if m not in ['VILLE','LIBELLE','code']:
          cols.append(pd.to_datetime(f"01-{month_map[m.split('-')[0]]}-{m.split('-')[1]}",dayfirst=True))
    else:
         cols.append(m)
 df.columns=cols
 df.drop(['VILLE','code'],axis=1,inplace=True)
 df = df.loc[:, ~df.columns.duplicated()]
 df=df[df['LIBELLE']=='GENERAL']
 df=df.drop('LIBELLE',axis=1)
 df=df.transpose()
 df=df.reset_index()
 df.columns=['Date','IPC']
 return df

#prepare 2007-2025:
def chainage():
    df_2006=prepare_2006()
    df_2017=pd.read_excel('backend/IPC.xlsx')
    df_2017=preparing_2017(df_2017)
    IPC_2017=df_2017[df_2017['Date']=='2017-12-01']['IPC'].values[0]
    IPC_2006=df_2006[df_2006['Date']=='2017-12-01']['IPC'].values[0]
    variation=(IPC_2017)/IPC_2006
    df_2006["IPC"]=round(df_2006["IPC"]*variation,1)
    df_2006=df_2006[df_2006['Date'] < '2017-01-01']
    df_finaly=pd.concat([df_2006,df_2017],ignore_index=True)
    df_finaly['Date']=pd.to_datetime(df_finaly['Date'])
    df_finaly=df_finaly.set_index('Date')
    return df_finaly


#ARIMA MODEL:
def model_ARIMA(df_finaly):
    train=df_finaly[:'2024-05-01']
    test=df_finaly['2024-05-01':]
    model=SARIMAX(train,order=(1,1,0),seasonal_order=(1,1,1,12))
    model_fit=model.fit()
    model_fit.save('backend/ARIMA_model.pkl')
    return test
#PLOT FORECAST
def data_to_ploty(df):
    lineplot=({
        
                 "x":df.index.strftime('%Y-%m-%d').tolist(),
                 "y":df['IPC'].values.tolist()
        })
    return lineplot

def arima_to_ploty(forecast,df_finaly):
    lineplot=({
        "forecast":{
                 "x":forecast.index.strftime('%Y-%m-%d').tolist(),
                 "y":forecast['predicted_mean'].values.tolist()
        },
        "actual":{
                    "x":df_finaly.index.strftime('%Y-%m-%d').tolist(),
                    "y":df_finaly['IPC'].tolist()
        }
    })
    return lineplot
#LSTM
def prepare_data(df_finaly,train_until="2024-05-01",seq_size=6,batch_size=1):
    train=df_finaly[:'2024-05-01']
    test=df_finaly['2024-05-01':]
    scaler=StandardScaler()
    scaler.fit(train)
    train_scaled=scaler.transform(train).reshape(-1,1)
    test_scaled=scaler.transform(test).reshape(-1,1)
    train_generator=TimeseriesGenerator(train_scaled,train_scaled,length=seq_size,batch_size=batch_size)
    test_generator=TimeseriesGenerator(test_scaled,test_scaled,length=seq_size,batch_size=batch_size)
    return train_generator,test_generator,scaler




def evaluate_model(model,test_generator,scaler):
  test_pred=model.predict(test_generator)
  test_pred=scaler.inverse_transform(test_pred)
  y_true=[]
  for i in range(len(test_generator)):
     x,y=test_generator[i]
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
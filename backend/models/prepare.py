import pandas as pd
import numpy as np
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
 excel_file = pd.ExcelFile('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC _2006_f.xlsx')
 sheet_names = excel_file.sheet_names

 data=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC _2006_f.xlsx',sheet_name=None)
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

def chainage():
    df_2006=prepare_2006()
    df_2017=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC.xlsx')
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
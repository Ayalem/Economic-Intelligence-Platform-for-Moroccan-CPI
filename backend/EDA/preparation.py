
import pandas as pd
import numpy as np

def preparing_df(df):
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
  return df



def df_city(df):
    df=preparing_df(df)
    df=df[df['libelle']=="GENERAL"]
    df=df[['Date','IPC','VILLE']]
    df=pd.pivot_table(index="Date",columns="VILLE",values="IPC",data=df)
    df=df.reset_index()
    return df



def df_national_general(df):
    df=df_city(df)
    df=df[['Date','National']]
    return df

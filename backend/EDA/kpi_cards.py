import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from . import preparation



#1.mean IPC
def mean_IPC(df):
    df_now=preparation.df_national_general(df)
    moyenne=df_now['National'].mean()
    return moyenne






#2.top 5 cities
def top5_cities(df):
    df_now=preparation.preparing_df(df)
    df_now_1=df_now[df_now['libelle']=="GENERAL"]
    top_5_cities=df_now_1.groupby('VILLE')['IPC'].mean().round(3).sort_values(ascending=False).head(5)
    top_5_cities=top_5_cities.reset_index()
    return top_5_cities





#3.top_5 categories
def top5_cat(df):
    df_now=preparation.preparing_df(df)
    df_now_cat=df_now[df_now['coicop'].str.len()==2]
    top_5_cat=df_now_cat.groupby('libelle')['IPC'].mean().round(3).sort_values(ascending=False).head()
    top_5_cat=top_5_cat.reset_index()
    return top_5_cat




#4.max IPC with date
def max_IPC(df):
   df_max=preparation.df_national_general(df)
   maximum_IPC=df_max[df_max['National']==df_max['National'].max()]
   return maximum_IPC




#5.average evolution:
def evolution(df):
    df_avg=preparation.df_national_general(df)
    df_avg['Date']=pd.to_datetime(df_avg['Date']).dt.year
    df_avg_year=df_avg.groupby('Date')['National'].mean().round(3)
    df_avg_year=df_avg_year.to_frame(name="IPC")
    df_avg_year['growth']=df_avg_year['IPC'].pct_change().round(3)
    df_avg_year.reset_index(inplace=True)
    return df_avg_year



def mean_evolution(df):
   df=evolution(df)
   evolution_mean=df['growth'].mean().round(2)
   return evolution_mean

def  evolution_year(df,year):
    df=evolution(df)
    evolution_year=df[df['Date']==year]['growth'].values[0]
    return evolution_year
def diff_evolution(df,year1,year2):
    evolution_year1=evolution_year(df,year1)
    evolution_year2=evolution_year(df,year2)
    diff_1_2=(evolution_year1-evolution_year2)/evolution_year1
    return diff_1_2
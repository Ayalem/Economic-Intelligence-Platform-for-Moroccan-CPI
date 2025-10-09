import pandas as pd
import numpy as np
import sys
import os

# add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from EDA import preparation
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
def cluster_categories(df):
    df=preparation.preparing_df(df)
    df_cat=df[df['coicop'].str.len()==2]
    df_cat=df_cat[df_cat['VILLE']=="National"]
    df_cat=df_cat.drop(["VILLE",'coicop'],axis=1)
    df_final=df_cat.pivot(index="libelle",columns="Date",values="IPC")
    return df_final

def cluster_cities(df):
    df=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC.xlsx')
    df_now=preparation.preparing_df(df)
    df_now_city=df_now[df_now['libelle']=="GENERAL"]
    df_now_city=df_now_city.drop(['coicop','libelle'],axis=1)
    df_now_city=df_now_city.pivot(index='VILLE',columns='Date',values='IPC')
    return df_now_city

def scaling(df):
    X=df.values
    scaler=StandardScaler()
    X_scaled=scaler.fit_transform(X)
    return X_scaled


def cluster(df,n_culsters=3):
      X_scaled=scaling(df)
      model = KMeans(n_clusters=n_culsters)
      model.fit(X_scaled)
      labels = model.labels_
      df['cluster']=labels
      return df
def reduce_dim(df,n_components=2):
     X_scaled=scaling(df.drop(columns=['cluster'], errors='ignore'))
     pca=PCA(n_components=n_components)
     components=pca.fit_transform(X_scaled)
     df_pca=pd.DataFrame(components,columns=['PC1','PC2'],index=df.index)
     df_pca['cluster']=df['cluster'].values
     return df_pca

def to_json_for_plotly(df_pca):
    data = []
    for cluster_id in df_pca['cluster'].unique():
        cluster_data = df_pca[df_pca['cluster'] == cluster_id]
        data.append({
            'x': cluster_data['PC1'].tolist(),
            'y': cluster_data['PC2'].tolist(),
            'name': f'Cluster {cluster_id}',
            'mode': 'markers',
            'text':[str(s).lower() for s in cluster_data.index.tolist()],
            'marker': {'size': 10},
        })
    return data
def cluster_summary(df_final):
    """
    df_final: dataframe avec 'cluster' et les colonnes IPC
    Retourne un dict { cluster_id: {statistiques} }
    """
    summary_json = {}
    for cluster_id in df_final['cluster'].unique():
        cluster_df = df_final[df_final['cluster'] == cluster_id]
        summary_json[int(cluster_id)] = {  # convertir clé en int natif
            "num_categories": len(cluster_df),
            "categories": cluster_df['text'].tolist() if 'text' in cluster_df else cluster_df.index.tolist(),
            "mean_PC1": float(cluster_df['PC1'].mean()),  
            "mean_PC2": float(cluster_df['PC2'].mean())
        }
    return summary_json




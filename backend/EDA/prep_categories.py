
import pandas as pd
import numpy as np
from . import preparation
def df_main_category(df):
    df_lvl1=df[df['coicop'].str.len()==2]
    return df_lvl1

#4.selection des categories principales format long avec coicop
def df_main_category_coicop(df):
    df=preparation.preparing_df(df)
    pivoted_table_coi=df.pivot_table(index='Date',columns=['VILLE','coicop'],values="IPC",sort=False)
    pivoted_table_coi_national=pivoted_table_coi['National']
    coicop_codes=list(pivoted_table_coi_national.columns.astype(str))
    sub_cat_1=[]
    for c in coicop_codes:
       if len(c)==2:#choosing main categories with coicop
          sub_cat_1.append(c)
    selected_df=pivoted_table_coi_national[[c for c in sub_cat_1 if c in pivoted_table_coi_national.columns]]
    return selected_df






#5.selection des categories principales format long avec libelle
def df_main_category_coicop_to_libele(df):
    df=df_main_category_coicop(df)
    coicop_to_libelle={
    "01":"PRODUITS ALIMENTAIRES ET BOISSONS NON ALCOOLISEES",
    "02":"BOISSONS ALCOOLISEES, TABAC ET STUPEFIANTS",
    "03":"ARTICLES D'HABILLEMENT ET CHAUSSURES",
    "04":"LOGEMENT, EAU, GAZ, ELECTRICITE ET AUTRES COMBUSTIBLES",
    "05":"MEUBLES, ARTICLES DE MENAGE ET ENTRETIEN COURANT DU FOYER",
    "06":"SANTE",
    "07":"TRANSPORTS",
    "08":"COMMUNICATIONS",
    "09":"LOISIRS ET CULTURE",
    "10":"ENSEIGNEMENT",
    "11":"RESTAURANTS ET HOTELS",
    "12":"BIENS ET SERVICES DIVERS"
}
    df.rename(columns=coicop_to_libelle,index=coicop_to_libelle,inplace=True)
    return df
from . import prep_categories
import pandas as pd
import numpy as np



#correlations des categories:
def category_corr(df,categories=["All"]):
    df=prep_categories.df_main_category_coicop_to_libele(df)
    if categories!=["All"]:
     df=df[categories]
     category_corr=df.corr()
    else:
        category_corr=df.corr()
    return category_corr

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
#verifier la stationarite de la serie avec test de dickey fuller
def check_stationarity(series,name=""):
    from statsmodels.tsa.stattools import adfuller,acf,pacf
    result=adfuller(series.dropna())
    p_value=result[1]
    print(f"ADF p-value pour {name}:{p_value:.3f}")
    if p_value<=0.05:
        print("La série est stationnaire (rejette Ho)")
        return 1
    else:
        print("La série n'est pas stationnaire (on accepte Ho)")
        return 0
#rendre stationnaire

def time_to_stationaire(x):
    for i in range(3):
     if check_stationarity(x)==1:
        return x
     else:
        x_diff=x.diff().dropna()
        check_stationarity(x_diff)
        return x_diff
#function to pick which two categories to choose :
def verify_correlation(cat1,cat2):
    from matplotlib.pyplot import plt
    from statsmodels.tsa.stattools import grangercausalitytests as gc
    cat1.name=coicop_to_libelle.get(cat1.name,cat1.name)
    cat2.name=coicop_to_libelle.get(cat2.name,cat2.name)

    #1verifie ccf correlation entre categorie 1 et categorie 2 :
    #1.1 stationarise la serie
    cat1=time_to_stationaire(cat1)
    cat2=time_to_stationaire(cat2)
    plt.plot(cat1,label=f"{cat1.name}")
    plt.plot(cat2,label=f"{cat2.name}")
    plt.legend()
    plt.title(f"Série temporelle:{cat1.name.lower()}et{cat2.name.lower()}")
    plt.grid(True)
    plt.show()
    #1.2 ccf:
    lags=range(-10,10)
    ccf_val=[cat1.corr(cat2.shift(lag))for lag in lags ]
    
    plt.title(f"cross correlation entre {cat1.name.lower()} et  {cat2.name.lower()}")
    plt.stem(ccf_val,lags)
    plt.show()
     #2verifie granger causality
    my_df=pd.DataFrame([cat1,cat2]).dropna()
    my_df=my_df.transpose()
    gc(my_df,maxlag=1,verbose=True)


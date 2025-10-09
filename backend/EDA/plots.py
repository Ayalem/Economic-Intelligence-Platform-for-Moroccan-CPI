
from . import prep_categories
from . import preparation
#6.categories plot:
def df_cat_to_json(df):
  df_cat=prep_categories.df_main_category_coicop_to_libele(df).reset_index()
  traces = []
  for cat in df_cat.columns.tolist():
        if cat !='Date':
            traces.append({
                "x": df_cat["Date"].tolist(),
                 "y": df_cat[cat].tolist(),
                 "name": cat,
                 "type": "scatter",
                 "mode": "lines"
            })
  return traces



#plot cities
def df_to_plotly_json(df):
    traces = []
    df=preparation.df_city(df)
    for city in df.columns:
        if city != 'Date':
            traces.append({
                "x": df["Date"].tolist(),
                "y": df[city].tolist(),
                "name": city,
                "type": "scatter",
                "mode": "lines"
            })
    return traces

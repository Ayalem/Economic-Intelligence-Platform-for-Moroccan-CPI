from flask import Flask ,jsonify,request
from flask_cors import CORS
import pandas as pd
from EDA import plots,kpi_cards,correlation_cards
from models import ARIMA,Prophet,LSTM,prepare
from models import HoltWinters as HW
from Clustering import clustering as c
app=Flask(__name__)
cors=CORS(app,origins="*")
@app.route("/",methods=["GET"])
def welcome():
    return '''


Welcome to this api:
         -/EDA/ipc_city:plot of IPC of all cities 
         -/EDA/ipc_cat:plot of IPC of all categories
         - /EDA/kpi:gives you metrics
         -/predict/arima/compare:comparison between test and pred ploty json
         -/predict/arima/future: 12 months future pred ploty json 
         -/predict/arima/metrics:mse rmse and mape
         -/predict/lstm/compare
          
'''
@app.route("/EDA/ipc_city",methods=['GET'])
def lineplot():
   df=pd.read_excel('backend/IPC.xlsx')
   traces=plots.df_to_plotly_json(df)
   return jsonify(traces)
@app.route("/EDA/ipc_cat",methods=["GET"])
def  plot():
    df=pd.read_excel('backend/IPC.xlsx')
    traces=plots.df_cat_to_json(df)
    return jsonify(traces)
@app.route("/EDA/kpi",methods=["GET"])
def home():
    df=pd.read_excel('backend/IPC.xlsx')
    response={
        "meanIPC":round(kpi_cards.mean_IPC(df),2),
        "meanEvolution":round(kpi_cards.mean_evolution(df),2),
        "maxIPC":kpi_cards.max_IPC(df).to_dict(orient="records"),
        "evolution2025":round(kpi_cards.evolution_year(df,2025)*100,2),
        "top5Categories":kpi_cards.top5_cat(df).to_dict(orient="records"),
        "top5Cities":kpi_cards.top5_cities(df).to_dict(orient="records"),
        "evolutionDiff ":round(kpi_cards.diff_evolution(df,2025,2024)*100,2)
    }
    return jsonify(response)

@app.route ("/predict/arima/compare",methods=["GET"])
def predict_arima():
     df_finaly=prepare.chainage()
     model_fit,test=ARIMA.model_ARIMA(df_finaly)
     forecast_test=ARIMA.arima_forecast(model_fit,len(test))
     lineplot=ARIMA.arima_to_ploty_compare(forecast_test,df_finaly)
     return jsonify(lineplot)
@app.route("/predict/arima/future",methods=["GET"])
def forecast_arima():
     df_finaly=prepare.chainage()
     model_fit,test=ARIMA.model_ARIMA(df_finaly)
     future_forecast=ARIMA.arima_forecast(model_fit,steps=len(test)+12)
     lineplot=ARIMA.arima_to_ploty_forecast(future_forecast,df_finaly)
     return jsonify(lineplot)
@app.route("/predict/arima/metrics",methods=["GET"])
def metrics_arima():
     df_finaly=prepare.chainage()
     model_fit,test=ARIMA.model_ARIMA(df_finaly)
     metrics=ARIMA.compute_metrics(model_fit,test=test)
     return jsonify(metrics)
#static lstm
@app.route("/predict/lstm/compare",methods=["GET"])
def predict_lstm():
    lineplot=LSTM.plot_compare()
    return jsonify(lineplot)
@app.route("/predict/lstm/future",methods=["GET"])
def forecast_lstm():
    l=LSTM.plot_forecast()
    return jsonify(l)
@app.route("/predict/lstm/metrics",methods=["GET"])
def metrics_lstm():
    metrics=LSTM.compute_metrics_static()
    return jsonify(metrics)
#Prophet
@app.route("/predict/prophet/compare",methods=["GET"])
def compare_prophet():
   df_finaly=prepare.chainage()
   m,test=Prophet.prepare_data(df_finaly)
   forecast=Prophet.predict_future(m,periods=len(test))
   lineplot=Prophet.ploty_compare(df_finaly,forecast)
   return jsonify(lineplot)
@app.route("/predict/prophet/future",methods=["GET"])
def forecast_prophet():
   df_finaly=prepare.chainage()
   m,test=Prophet.prepare_data(df_finaly)
   forecast=Prophet.predict_future(m,periods=len(test)+12)
   lineplot=Prophet.ploty_forecast(df_finaly,forecast)
   return jsonify(lineplot)
@app.route("/predict/prophet/metrics",methods=["GET"])
def metrics_prophet():
    df_finaly=prepare.chainage()
    m,test=Prophet.prepare_data(df_finaly)
    metrics=Prophet.compute_metrics(m,test)
    return jsonify(metrics)
#holt winters:
@app.route ("/predict/hw/compare",methods=["GET"])
def predict_hw():
     df_finaly=prepare.chainage()
     model_fit,test=HW.prepare_data(df_finaly)
     forecast_test=HW.forecast(model_fit,len(test))
     lineplot=HW.winter_to_ploty_compare(forecast_test,df_finaly)
     return jsonify(lineplot)
@app.route("/predict/hw/future",methods=["GET"])
def forecast_hw():
     df_finaly=prepare.chainage()
     model_fit,test=HW.prepare_data(df_finaly)
     forecast_test=HW.forecast(model_fit,len(test)+12)
     lineplot=HW.winter_to_ploty_forecast(forecast_test,df_finaly)
     return jsonify(lineplot)
@app.route("/predict/hw/metrics",methods=["GET"])
def metrics_hw():
     df_finaly=prepare.chainage()
     model_fit,test=HW.prepare_data(df_finaly)
     metrics=HW.compute_metrics(model_fit,test)
     return jsonify(metrics)
@app.route("/api/cities",methods=["GET"])
def get_cities():
   df=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC.xlsx')
   df_final =c.cluster_cities(df)
   df_final=c.cluster(df_final)
   df_pca = c.reduce_dim(df_final)
   plot_data = c.cluster_categoriesto_json_for_plotly(df_pca)
   summary_json=c.cluster_summary(df_pca)
   data={
    "plot":plot_data,
    "summary":summary_json
    }
   return jsonify(data)
    
@app.route("/api/categories", methods=["GET"])
def get_categories():
    df=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC.xlsx')
    df_final = c.cluster_categories(df)
    df_final=c.cluster(df_final)
    df_pca = c.reduce_dim(df_final)
    plot_data = c.to_json_for_plotly(df_pca)
    summary_json=c.cluster_summary(df_pca)
    data={
    "plot":plot_data,
    "summary":summary_json
    }
    return jsonify(data)
@app.route("/api/correlation",methods=["POST"])
def get_correlations():
    data=request.get_json()
    categoryA=data.get('categoryA','').upper()
    categoryB=data.get('categoryB','').upper()
    df=pd.read_excel('/Users/ayalemzouri/Desktop/Academics/PFA_2025/Dashboard/backend/IPC.xlsx')
    datas=correlation_cards.category_corr(df,[categoryA,categoryB])
    Cdata={
        "correlation":datas.values.tolist(),
        "categories":datas.columns.tolist(),
        
    }
    return jsonify(Cdata)


  

if __name__=="__main__":
    app.run(debug=True,port=8000)

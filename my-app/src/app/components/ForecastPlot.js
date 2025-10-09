'use client';
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });
export default function ForecastPlot({ model,mode }) {
  const [data, setData] = useState(null);
const modelColors={
  arima: 'red',
  hw: '#3CB371',
  lstm: '#9C27B0'
};

const modelColor = modelColors[model];

  useEffect(() => {
    async function fetchData() {
      const res = await fetch(`http://127.0.0.1:8000/predict/${model}/${mode}`);
      const json = await res.json();
      setData(json);
    }
    fetchData();
  }, [model]);


  if (!data) return <p>Loading...</p>;
const useCombinedBand = true; 
 let  plotData = [
    {
      x: data.forecast.x,
      y: data.forecast.y,
      type: 'scatter',
      mode:'lines',
      name: `${model.toUpperCase()} Forecast`,
      line: { color: modelColor,width:2 },
    },
    {
      x: data.actual.x,
      y: data.actual.y,
      type: 'scatter',
      name: 'Actual',
      line: { color: 'black' },
    },
  ];

  if (model === 'prophet' && data.forecast.yhat_upper && data.forecast.yhat_lower) {
  
 if(!useCombinedBand){
  plotData=[
         {
      x: data.forecast.ds,
      y: data.forecast.yhat,
      type: 'scatter',
      mode:"lines",
      name: `${model.toUpperCase()} Forecast`,
      line: { color: 'blue', width: 2 },
    },
    {
      x: data.actual.ds,
      y: data.actual.y,
      type: 'scatter',
      mode:"lines",
      name: 'Actual',
      line: { color: 'black',size: 4 },
    },
    {
        x: data.forecast.ds,
        y: data.forecast.yhat_upper,
        type: 'scatter',
        name: 'Upper Bound',
         fill: 'toself',
        fillcolor: 'rgba(0, 116, 217, 0.2)',
        line: {color: 'transparent'},
        mode:"lines",
      
        showlegend: true,
      },
      {
        x: data.forecast.ds,
        y: data.forecast.yhat_lower,
        type: 'scatter',
        name: 'Lower Bound',
        fill: 'toself',
        fillcolor: 'rgba(0, 116, 217, 0.2)',
        line: {color: 'transparent'},
        mode:"lines",
        
        showlegend: true,
      }
    ];
      
   
  }
 else{
  plotData=[
         {
      x: data.forecast.ds,
      y: data.forecast.yhat,
      type: 'scatter',
      mode:"lines",
      name: `${model.toUpperCase()} Forecast`,
      line: { color: 'blue', width: 2 },
    },
    {
      x: data.actual.ds,
      y: data.actual.y,
      type: 'scatter',
      mode:"lines",
      name: 'Actual',
      line: { color: 'black',size: 4 },
    },
    {
    x: [...data.forecast.ds, ...data.forecast.ds.slice().reverse()],
    y: [...data.forecast.yhat_upper, ...data.forecast.yhat_lower.slice().reverse()],
    type: 'scatter',
    fill: 'toself',
    fillcolor: 'rgba(0, 116, 217, 0.2)',
    line: { color: 'transparent' },
    name: 'Confidence Interval',
    showlegend: true
  }
  ];
}
  }
  return (
    <Plot
      data={plotData}
      layout={{
        title: `${model.toUpperCase()} Forecast`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'IPC' },
        autosize:true,
          legend: {
      font: { size: 10 },          
      orientation: 'h',            
      x: 0.5,
      y: 1.1,
      xanchor: 'center',
      yanchor: 'bottom'

    },
      }}
       style={{ width: '100%', height: '80%' }}
       useResizeHandler={true}
    />
  );

}

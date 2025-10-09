'use client';
import { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });
export default function ForecastPlot({ model,future }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch(`http://127.0.0.1:8000/predict/${model}/${future}`);
      const json = await res.json();
      setData(json);
    }
    fetchData();
  }, [model]);

  if (!data) return <p>Loading...</p>;

 let  plotData = [
    {
      x: data.forecast.x,
      y: data.forecast.y,
      type: 'scatter',
      mode:'lines',
      name: `${model.toUpperCase()} Forecast`,
      line: { color: 'red' },
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
        showlegend: false,
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
         hoverinfo: 'skip',
        showlegend: false,
      }
    ];
      
   
  }

  return (
    <Plot
      data={plotData}
      layout={{
        title: `${model.toUpperCase()} Forecast`,
        xaxis: { title: 'Date' },
        yaxis: { title: 'IPC' },
          legend: {
      font: { size: 10 },          
      orientation: 'h',            
      x: 0.5,
      y: 1.1,
      xanchor: 'center',
      yanchor: 'bottom'
    },
      }}
       style={{ width: '75%', height: '80%' }}
    />
  );
}

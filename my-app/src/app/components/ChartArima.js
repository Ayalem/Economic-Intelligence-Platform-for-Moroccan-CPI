'use client'
import dynamic from 'next/dynamic';
import {useState,useEffect} from 'react';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });
export default  function ChartArima(){
    const [actual,setActual]=useState({x:[],y:[]});
    const [forecast,setForecast]=useState({x:[],y:[]});
    useEffect(()=>{
        fetch("http://127.0.0.1:8000/arima")
            .then(response=>response.json())
            .then(data=>{
                setActual(data.actual),
                setForecast(data.forecast)
            })
    },[])
 return(
    <div>
    <Plot
        data={[
          {
            x:actual.x,
            y: actual.y,
            type: 'scatter',
            mode: 'lines',
            marker: {color: 'green'},
          },
           {
          x: forecast.x,
          y:forecast.y,
          type: "scatter",
          mode: "lines",
          name: "Forecast",
          line: { color: "red" }
        }
        ]}
        layout={
        {
            title:"évolution de l'IPC ",
            yaxis:{title:"IPC"},
            xaxis:{title:"Date"},
            legend: {
      font: { size: 10 },          
      orientation: 'h',            
      x: 0.5,
      y: 1.1,
      xanchor: 'center',
      yanchor: 'bottom'
    },
    margin: { t: 60, b: 40 },     
  }}
   style={{ width: '75%', height: '80%' }}
    />
 </div>
 );
}
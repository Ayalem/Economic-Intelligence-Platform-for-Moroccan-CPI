'use client'
import dynamic from 'next/dynamic';
import { useState, useEffect } from 'react';

const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function Charts() {
  const [datas, setDatas] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/EDA/ipc_city")
      .then(response => response.json())
      .then(rawDatas => {
        const blueColors = [
           '#1e40af', '#3b82f6','#6366f1', '#9333ea','#10b981', '#f59e0b', '#ef4444' 
        ];
  
  
 
  

        const formattedDatas = rawDatas.map((trace, idx) => ({
          ...trace,
          type: 'scatter',
          mode: 'lines',
          line: { color: blueColors[idx % blueColors.length], width: 1,opacity: 0.7 }
          
        }));

        setDatas(formattedDatas);
      })
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  return (
    <div className="rounded-2xl border border-gray-200 bg-white px-5 py-5 shadow-md dark:border-gray-800 dark:bg-white/[0.03]">
      <div className="mb-4">
        <h3 className="text-lg font-semibold text-gray-800 dark:text-white/90">
          Évolution de l'IPC par ville
        </h3>
        <p className="text-sm text-gray-500 dark:text-gray-400">
          Analyse des variations de l'indice des prix à la consommation par ville
        </p>
      </div>

      <div className="w-full h-[400px]">
        <Plot
          data={datas}
          layout={{
            autosize: true,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
            font: {
              family: 'Inter, sans-serif',
              size: 12,
              color: '#374151'
            },
            margin: { t: 60, b: 50, l: 50, r: 30 },
            title: {
              text: '',
              font: {
                size: 16,
                color: '#1f2937'
              }
            },
            xaxis: {
              title: 'Date',
              tickangle: -45,
              tickfont: { size: 11 },
              gridcolor: 'rgba(200, 200, 200, 0.2)',
              zeroline: false
            },
            yaxis: {
              title: 'IPC',
              tickfont: { size: 11 },
              gridcolor: 'rgba(200, 200, 200, 0.2)',
              zeroline: false
            },
            legend: {
              orientation: 'h',
              y: -0.3,
              x: 0.5,
              xanchor: 'center',
              font: { size: 10 }
            },
          }}
          config={{
            displayModeBar: false,
            responsive: true
          }}
          style={{ width: '100%', height: '100%' }}
        />
      </div>
    </div>
  );
}

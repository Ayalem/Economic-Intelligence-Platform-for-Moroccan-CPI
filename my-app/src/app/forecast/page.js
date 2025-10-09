'use client';

import { useState } from 'react';
import ForecastPlot from "../components/ForecastPlot";
import MetricsDisplay from "../components/MetricsDisplay";
import ToggleButton from "../components/ToggleButton";
import { BarChart4, LineChart, Gauge } from 'lucide-react'; 

export default function ForecastPage() {
  const [selectedModel, setSelectedModel] = useState("ARIMA");

  const handleModelChange = (e) => {
    setSelectedModel(e.target.value);
  };

  return (
    <div className="min-h-screen px-10 py-12 bg-gray-50">
      <div className="max-w-6xl mx-auto">
       
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-4xl font-bold text-gray-800">📈 Forecast Dashboard</h1>
            <p className="text-gray-500 mt-1">Compare models, view forecasts, and evaluate metrics.</p>
          </div>
          <ToggleButton selectedModel={selectedModel} onChange={handleModelChange} />
        </div>

        {/* Forecast Section */}
        <div className="bg-white rounded-2xl shadow p-6 mb-8">
          <div className="flex items-center mb-4">
            <LineChart className="text-blue-500 mr-2" />
            <h2 className="text-xl font-semibold text-gray-700">Forecast: Next 12 Months</h2>
          </div>
          <ForecastPlot model={selectedModel.toLowerCase()} mode="future" />
        </div>


        <div className="bg-white rounded-2xl shadow p-6 mb-8">
          <div className="flex items-center mb-4">
            <BarChart4 className="text-green-500 mr-2" />
            <h2 className="text-xl font-semibold text-gray-700">Model Comparison: Actual vs Predicted</h2>
          </div>
          <ForecastPlot model={selectedModel.toLowerCase()} mode="compare" />
        </div>

        <div className="bg-white rounded-2xl shadow p-6 mb-8">
          <div className="flex items-center mb-4">
            <Gauge className="text-purple-500 mr-2" />
            <h2 className="text-xl font-semibold text-gray-700">Performance Metrics</h2>
          </div>
          <MetricsDisplay model={selectedModel.toLowerCase()} />
        </div>
      </div>
    </div>
  );
}

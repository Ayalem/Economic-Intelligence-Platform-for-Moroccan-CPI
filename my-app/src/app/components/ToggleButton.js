'use client'
import {useState,useEffect} from 'react'
export default function ToggleButton({selectedModel,onChange}){
const models=["ARIMA","HW","LSTM","Prophet"]
return (
    <div className="flex gap-4 items-center">
      <label className="text-sm font-medium text-gray-600">Select Model:</label>
      <select
        value={selectedModel}
        onChange={onChange}
        className="p-2 rounded border border-gray-300"
      >
        {models.map((model) => (
          <option key={model} value={model}>
            {model.toUpperCase()}
          </option>
        ))}
      </select>
    </div>
  );
}

'use client'
import {useEffect,useState} from 'react';

export default function MetricsDisplay({model}) {
 const [data,setData]=useState(null);
const [error, setError] = useState(null);

     useEffect(()=>{
        async function fetchData(){
            try{
                const res = await fetch(`http://127.0.0.1:8000/predict/${model}/metrics`);
                if (!res.ok){
                    throw new Error("failed to fetch metrics")
                }
                const json = await res.json();
                setData(json);
                setError(null);
            }catch(err){
                 setError(err.message);
                 setData(null);
            }
                
    }
    fetchData();
     },[model]);
        if (error) {
    return <p className="text-red-600 mt-4">Error: {error}</p>;
  }
       if (!data) {
    return <p className="mt-4 text-gray-500 italic">Loading metrics...</p>;
  }
    
  return (
    <div className="bg-gray-100 p-4 rounded shadow mt-4">
      <h3 className="text-lg font-semibold mb-2">Metrics</h3>
      <ul className="list-disc list-inside text-sm">
        {Object.entries(data).map(([key, value]) => (
          <li key={key}>
            <strong>{key.toUpperCase()}:</strong> {value.toFixed(3)}
          </li>
        ))}
      </ul>
    </div>
  );
}

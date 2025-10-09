'use client'
import {useState,useEffect} from 'react';
import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });
export default  function ClusteringChart(){
 const [ClusterData,SetClusterData]=useState(null);
 const [error,setError]=useState(null);
 const clusterColors = ["#D6EAF8", "#D5F5E3", "#FCF3CF", "#F5B7B1", "#E8DAEF"]; 
useEffect(
    ()=>{
        async function fetchData(){
            try{
            const res= await fetch("http://127.0.0.1:8000/api/categories");
            const json= await res.json();
            SetClusterData(json);
            }catch(err){
                setError(err);
            }
           
            
        }
        fetchData();},[])
 if (error) return <p>Error: {error.message}</p>;
  if (!ClusterData) return <p>Loading...</p>; 
    

    return(
        <div>
        <div>
             <Plot data={ClusterData.plot}
             layout={{ title: "Clusters", autosize: true }}/>
              
      
         
        </div>
        <div>
        <h2>Résumé des Clusters</h2>
        <table style={{ borderCollapse: "collapse", width: "100%", textAlign: "left" }}>
          <thead>
            <tr style={{ backgroundColor: "#2E86C1", color: "white" }}>
              <th style={{ padding: "8px" }}>Cluster</th>
              <th style={{ padding: "8px" }}># Catégories</th>
              <th style={{ padding: "8px" }}>Moyenne PC1</th>
              <th style={{ padding: "8px" }}>Moyenne PC2</th>
              <th style={{ padding: "8px" }}>Catégories</th>
            </tr>
          </thead>
          <tbody>
            {Object.entries(ClusterData.summary).map(([clusterId, clusterInfo], index) => (
              <tr key={clusterId} style={{ backgroundColor: clusterColors[index % clusterColors.length] }}>
                <td style={{ padding: "8px" }}>Cluster {clusterId}</td>
                <td style={{ padding: "8px" }}>{clusterInfo.num_categories}</td>
                <td style={{ padding: "8px" }}>{clusterInfo.mean_PC1.toFixed(2)}</td>
                <td style={{ padding: "8px" }}>{clusterInfo.mean_PC2.toFixed(2)}</td>
                <td style={{ padding: "8px", maxWidth: "300px", whiteSpace: "pre-wrap", overflowY: "auto", maxHeight: "150px" }}>
                  {clusterInfo.categories.join(", ")}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}


   

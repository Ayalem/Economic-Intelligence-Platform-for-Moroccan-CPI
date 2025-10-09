'use client'
import {useState,useEffect} from 'react';
import CorrelationToggle from './CorrelationToggle';
import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });
export default function CorrelationCard(){
 const [categoryA,setCategoryA]=useState("PRODUITS ALIMENTAIRES ET BOISSONS NON ALCOOLISEES");
 const [categoryB,setCategoryB]=useState("TRANSPORTS");
 const [Cdata,setCdata]=useState(null);
const [error, setError] = useState(null);


 const handleCatChangeA=(e)=>{
    setCategoryA(e.target.value);
 };
 const handleCatChangeB=(e)=>{
    setCategoryB(e.target.value);
 };
useEffect(()=>{
    async function fetchData(){
        try{
           const res=await fetch("http://127.0.0.1:8000/api/correlation",{
           method:'POST',
           headers:{"Content-Type":'application/json'},
           body: JSON.stringify({categoryA,categoryB}),
           });
         if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
         const data=await res.json();
         setCdata(data);
         setError(null);
    }catch(err){
       setError(err.message);
       setCdata(null);
    }
}
    if (categoryA &&categoryB){
        fetchData()
    }
},[categoryA,categoryB]);


    return(
        <div className=" max-w-5xl mx-auto p-6 bg-white shadow-lg rounded-2xl">
            <h2 className='text-xl font-semibold mb-4 text-center '>Carte de Corrélation</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                  <CorrelationToggle  className="w-full" selectedCat={categoryA} onChange={handleCatChangeA}/>
                  <CorrelationToggle  className="w-full" selectedCat={categoryB} onChange={handleCatChangeB}/>
            </div>
           
                {error && (
                    <div className="text-red-600 font-medium  text-center mb-4">
                        Error:{error}
                    </div>
                )}

                {
                    Cdata &&(
                        <div className="overflow-x-auto">
                            <Plot
                        data={[
                            {
                            z:Cdata.correlation,
                            x:Cdata.categories,
                            y:Cdata.categories,
                            type:'heatmap',
                            colorscale:[
                                 [0, '#e0f3ff'],  
                                 [0.5, '#69b3e7'], 
                                 [1, '#08306b']    
                             ],
                            colorbar: { title: 'Correlation', titleside: 'right' },
                            text: Cdata.correlation.map(row => row.map(val => val.toFixed(2))),
                            texttemplate: '%{text}',
                            textfont: { size: 12, color: 'black' },
                            },
                            
                           
                        ]}
                        layout={{
                            title:{
                                text:"carte thermique de corrélation",
                                font: { size: 18 },
                                  x: 0.5,
                            },
                            autosize:true
                            

                        }}
                         style={{ width: '100%'}}
                         config={{ responsive: true }}
                        />
                           
                        </div>
                        

                    )
                }
            </div>
      
        

    );
}
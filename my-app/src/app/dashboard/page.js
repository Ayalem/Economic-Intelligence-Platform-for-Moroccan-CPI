'use client'
import {useState,useEffect} from 'react';
import Charts from "../components/Charts";

import CharTest from "../components/CharTest";
import Table from "../components/Table";
import MeanIpcCard from '../components/MeanIpcCard';
import NationalEvolutionCard from '../components/NationalEvolutionCard';
import CorrelationCard from '../components/CorrelationCard';
export default  function dashboard(){

    const [Kpi, setKpi] = useState({
    maxIPC: [],
    evolutionDiff:[],
    meanIPC: [],
    meanEvolution: [],
    evolution2025: [],
    top5Categories: [],
    top5Cities: []
  });

  useEffect(() => {
    fetch("http://127.0.0.1:8000/EDA/kpi")
      .then(response => response.json())
      .then(data => setKpi(data))
      .catch(err => console.error("Error fetching KPI data:", err));
  }, []);
    return (
        <div className=" p-20" >
        <h1>PAGE DASHBOARD</h1>
        <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-5 p-5'>
         <Charts/>
         <Table data={Kpi.top5Cities} title="Les 5 villes ayant l’IPC le plus élevé"/>
        <CharTest/>
        <Table data={Kpi.top5Categories} title="les 5 catégories ayant l'IPC le plus élevé" nameKey = "libelle" valueKey = "IPC"/>
       <MeanIpcCard evolutionDiff={Kpi.meanEvolution} meanIPC={Kpi.meanIPC} title="indice moyen IPC"/>
       <NationalEvolutionCard evolutionDiff={Kpi.evolutionDiff} evolution2025={Kpi.evolution2025} />
       <CorrelationCard/>
        </div>
        
        </div>
        
    );
}
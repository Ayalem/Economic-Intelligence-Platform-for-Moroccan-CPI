'use client'
import Image from "next/image";

import Link from 'next/link';
import { ArrowRight, BarChart3, LineChart, Network } from "lucide-react";

export default function Home() {


  return (
    <div className="p-20 flex-col justify-between">
      


    <div className="min-h-screen bg-gray-50 text-gray-900">
      
     
      <section className="flex flex-col items-center justify-center py-24 bg-gradient-to-r from-blue-500 to-blue-700 text-white text-center">
        <h1 className="text-5xl font-bold mb-6">Indice des Prix à la Consommation (IPC)</h1>
        <p className="text-xl max-w-2xl mb-8">
          Un tableau de bord interactif pour analyser, prévoir et comprendre les tendances de l’inflation.
        </p>
        <a 
          href="/dashboard" 
          className="bg-white text-blue-700 px-6 py-3 rounded-2xl font-semibold shadow hover:bg-gray-100 transition"
        >
          Explorer le Dashboard
        </a>
      </section>


      <section className="py-16 px-8 max-w-5xl mx-auto text-center">
        <h2 className="text-3xl font-semibold mb-4">Pourquoi l’IPC ?</h2>
        <p className="text-lg text-gray-700 leading-relaxed">
          L’Indice des Prix à la Consommation mesure l’évolution du coût de la vie. 
          Ce projet combine <span className="font-bold">statistiques, Machine Learning et visualisations interactives</span> 
          pour offrir une plateforme complète d’intelligence économique.
        </p>
      </section>

     
      <section className="py-16 bg-gray-100">
        <h2 className="text-3xl font-semibold text-center mb-12">Fonctionnalités</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto px-6">
          
          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
            <LineChart className="w-10 h-10 text-blue-600 mb-4"/>
            <h3 className="text-xl font-semibold mb-2">Prévisions</h3>
            <p>Modèles ARIMA, Prophet et LSTM pour anticiper les tendances de l’inflation.</p>
          </div>
          
          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
            <BarChart3 className="w-10 h-10 text-green-600 mb-4"/>
            <h3 className="text-xl font-semibold mb-2">Analyses de Corrélation</h3>
            <p>Visualisez les relations entre catégories et régions avec des matrices et graphes.</p>
          </div>

          <div className="bg-white p-6 rounded-2xl shadow hover:shadow-lg transition">
            <Network className="w-10 h-10 text-indigo-600 mb-4"/>
            <h3 className="text-xl font-semibold mb-2">Clustering</h3>
            <p>Segmentez les régions et catégories selon leurs comportements d’inflation.</p>
          </div>

        </div>
      </section>

    
      <footer className="py-6 text-center text-gray-600">
        <p>📊 Données basées sur l’IPC national · Projet académique · Aya Lemzouri</p>
      </footer>

    </div>
  

  
    </div>
  );
}

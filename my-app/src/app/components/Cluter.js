'use client';
import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';
const Plot = dynamic(() => import('react-plotly.js'), { ssr: false });

export default function Cluter() {
  const [ClusterData, SetClusterData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/categories");
        const json = await res.json();
        SetClusterData(json);
      } catch (err) {
        setError(err);
      }
    }
    fetchData();
  }, []);

  if (error) return <p className="text-red-500">Erreur : {error.message}</p>;
  if (!ClusterData) return <p className="text-gray-500">Chargement...</p>;


  return (
    <div className="p-6 font-sans bg-gray-50 min-h-screen">
      <h1 className="text-2xl font-bold mb-6">Classification des catégories par évolution de l'IPC</h1>

      {/* Plot */}
      <div className="mb-8 bg-white p-4 rounded shadow-lg">
        <Plot
          data={ClusterData.plot}
          layout={{
            title: { text: "Clusters", font: { size: 24 } },
            autosize: true,
            xaxis: { title: "PC1" },
            yaxis: { title: "PC2" },
            legend: { orientation: "h", x: 0.5, xanchor: "center", y: -0.2 },
          }}
          style={{ width: "100%", height: "500px" }}
        />
      </div>

      {/* Table */}
      <div className="bg-white p-4 rounded shadow-lg">
        <h2 className="text-xl font-semibold mb-4">Résumé des Clusters</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-blue-600 text-white">
              <tr>
                <th className="px-4 py-2 text-left">Cluster</th>
                <th className="px-4 py-2 text-left"># Catégories</th>
                <th className="px-4 py-2 text-left">Moyenne PC1</th>
                <th className="px-4 py-2 text-left">Moyenne PC2</th>
                <th className="px-4 py-2 text-left">Catégories</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {Object.entries(ClusterData.summary).map(([clusterId, clusterInfo], index) => (
                <tr key={clusterId} className={index % 2 === 0 ? "bg-gray-50" : ""}>
                  <td className="px-4 py-2 font-medium">Cluster {clusterId}</td>
                  <td className="px-4 py-2">{clusterInfo.num_categories}</td>
                  <td className="px-4 py-2">{clusterInfo.mean_PC1.toFixed(2)}</td>
                  <td className="px-4 py-2">{clusterInfo.mean_PC2.toFixed(2)}</td>
                 <td className="px-4 py-2 border">
  <div className="flex flex-wrap gap-2">
    {clusterInfo.categories.map((cat, idx) => (
      <span
        key={idx}
        className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs"
      >
        {cat}
      </span>
    ))}
  </div>
</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

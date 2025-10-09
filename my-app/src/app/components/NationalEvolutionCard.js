import { ArrowUpRight, ArrowDownRight } from 'lucide-react';

export default function NationalEvolutionCard({ evolution2025, evolutionDiff }) {
  const roundedEvo = evolution2025 ;

  const isPositive = evolution2025 >= 0;
  const iconColor = isPositive ? 'text-green-600' : 'text-red-600';
  const diffLabel = evolutionDiff > 0 ? "hausse" : "baisse";

  return (
    <div className="rounded-2xl shadow-md bg-white p-6 w-full max-w-md border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-semibold text-gray-700">
            Évolution nationale de l’IPC  2025
          </h3>
          <p className={`mt-1 text-2xl font-bold ${iconColor}`}>
            {isPositive ? '+' : ''}{roundedEvo}%
          </p>
          <p className="text-sm text-gray-500 mt-1">
            Par rapport à l’année 2024
          </p>
        </div>
        <div className="text-4xl">
          {isPositive ? <ArrowUpRight className="text-green-600" /> : <ArrowDownRight className="text-red-500" />}
        </div>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        L’évolution a enregistré une {diffLabel} de <span className="font-semibold"> {evolutionDiff} points</span> par rapport à l’évolution précédente.
      </div>
    </div>
  );
}

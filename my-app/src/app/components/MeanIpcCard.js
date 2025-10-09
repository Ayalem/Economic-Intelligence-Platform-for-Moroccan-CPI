import { ArrowUpRight, ArrowDownRight } from 'lucide-react'; // optional icons

export default function MeanIpcCard({ meanIPC, evolutionDiff,title="" }) {
  const roundedMean = meanIPC;
  const roundedDiff =evolutionDiff;

  const isPositive = evolutionDiff > 0;

  return (
    <div className="rounded-2xl border border-gray-200 bg-white px-6 py-5 shadow-sm dark:border-gray-800 dark:bg-white/[0.03]">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-lg font-semibold text-gray-700">{title}</h4>
          <p className="mt-1 text-2xl font-semibold text-gray-900 dark:text-white">
            {roundedMean}
          </p>
          <p className={`mt-1 text-sm font-bold ${isPositive ? "text-green-600" : "text-red-500"}`}>
            {isPositive ? "+" : ""}{roundedDiff}% par rapport à l’année dernière
          </p>
        </div>
        <div className={`text-3xl ${isPositive ? "text-green-600" : "text-red-500"}`}>
          {isPositive ? <ArrowUpRight /> : <ArrowDownRight />}
        </div>
      </div>
    </div>
  );
}


'use client';
import React from 'react';

export default function KpiTable({ title, subtitle = '', data = [], nameKey = "VILLE", valueKey = "IPC" }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="p-6 border border-gray-200 rounded-2xl shadow-sm bg-white dark:bg-white/[0.03]">
        <h2 className="text-lg font-semibold text-gray-700 dark:text-white">{title}</h2>
        <p className="text-sm text-gray-500">{subtitle}</p>
        <p className="mt-4 text-gray-400">No data available.</p>
      </div>
    );
  }

  return (
    <div className="p-6 border border-gray-200 rounded-2xl shadow-sm bg-white dark:bg-white/[0.03]">
      <h2 className="text-lg font-semibold text-gray-700 dark:text-white">{title}</h2>
      <p className="text-sm text-gray-500 mb-4">{subtitle}</p>

      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200 text-sm">
          <thead className="bg-gray-50 dark:bg-white/[0.08]">
            <tr>
              <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">#</th>
              <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">{nameKey}</th>
              <th className="px-4 py-2 text-left font-medium text-gray-600 dark:text-gray-300">{valueKey}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
            {data.map((item, index) => (
              <tr key={index} className="hover:bg-gray-50 dark:hover:bg-white/[0.05]">
                <td className="px-4 py-2 font-semibold text-gray-700 dark:text-gray-200">{index + 1}</td>
                <td className="px-4 py-2 text-gray-600 dark:text-gray-300">{item[nameKey].toLowerCase()}</td>
                <td className="px-4 py-2 text-gray-600 dark:text-gray-300">{item[valueKey]?.toFixed(2)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

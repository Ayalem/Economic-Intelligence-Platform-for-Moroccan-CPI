'use client'

import Link from "next/link";
import { useState } from "react";
import { MdMenu, MdDashboard, MdClose } from "react-icons/md";
import { GrCluster } from "react-icons/gr";
import { FaMagnifyingGlassChart } from "react-icons/fa6";

import { LuChartLine, LuBarChartHorizontal } from "react-icons/lu";
export default function Navbar() {
  const [isOpen, setIsOpen] = useState(false);

  const handleOpen = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="relative z-50">
      {/* Menu Button */}
      <button
        className="p-4 fixed top-4 left-4 z-50 bg-white text-gray-800 rounded-md shadow-lg"
        onClick={handleOpen}
      >
        <MdMenu size={24} />
      </button>

      {/* Sidebar */}
      {isOpen && (
        <nav className="fixed top-0 left-0 h-full w-64 bg-white text-gray-800  shadow-2xl z-40 flex flex-col px-4 pt-10 transition-all duration-300">
          {/* Close Button */}
          <button
            className="absolute top-4 right-4 text-gray-800 "
            onClick={handleOpen}
          >
            <MdClose size={24} />
          </button>

          {/* Nav Items */}
          <ul className="flex flex-col gap-4 mt-8">
            <li className="hover:bg-[#4286f5] px-4 py-3 rounded-md transition">
              <Link href="/" onClick={handleOpen} className="flex items-center gap-3">
                <MdDashboard size={20} />
                <span>Home</span>
              </Link>
            </li>

            <li className="hover:bg-[#4286f5] px-4 py-3 rounded-md transition">
              <Link href="/dashboard" onClick={handleOpen} className="flex items-center gap-3">
                <LuChartLine size={20} />
                <span>Dashboard</span>
              </Link>
            </li>

            <li className="hover:bg-[#4286f5] px-4 py-3 rounded-md transition">
              <Link href="/forecast" onClick={handleOpen} className="flex items-center gap-3">
                <FaMagnifyingGlassChart size={20}/>
                <span>Forecast</span>
              </Link>
            </li>

            <li className="hover:bg-[#4286f5] px-4 py-3 rounded-md transition">
              <Link href="/clustering" onClick={handleOpen} className="flex items-center gap-3">
               <GrCluster size={20}/>

                <span>Clustering</span>
              </Link>
            </li>
          </ul>
        </nav>
      )}
    </div>
  );
}

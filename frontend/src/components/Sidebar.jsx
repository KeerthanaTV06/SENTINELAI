import React from 'react'
import { NavLink } from 'react-router-dom'
import { Home, Database, Layers, Activity, PieChart } from 'lucide-react'

const Sidebar = () => {
  const links = [
    { to: '/dashboard', label: 'Dashboard', icon: Home },
    { to: '/datasets', label: 'Datasets', icon: Database },
    { to: '/models', label: 'Models', icon: Layers },
    { to: '/predict', label: 'Predict', icon: Activity },
    { to: '/explain', label: 'Explain', icon: PieChart },
    { to: '/reports', label: 'Reports', icon: PieChart },
  ]

  return (
    <aside className="w-64 bg-gradient-to-b from-black/60 via-gray-900 to-black p-4 text-gray-200">
      <div className="mb-6 text-center">
        <h1 className="text-xl font-semibold">SENTINEL-AI</h1>
        <p className="text-xs text-gray-400">Threat Intelligence</p>
      </div>

      <nav className="space-y-2">
        {links.map((l) => (
          <NavLink key={l.to} to={l.to} className={({ isActive }) => `flex items-center gap-3 p-2 rounded-md hover:bg-gray-800 ${isActive ? 'bg-blue-900/40' : ''}`}>
            <l.icon />
            <span>{l.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="mt-auto pt-6 text-xs text-gray-500">
        <div>v0.1.0</div>
      </div>
    </aside>
  )
}

export default Sidebar

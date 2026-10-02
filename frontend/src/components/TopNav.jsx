import React from 'react'

const TopNav = () => {
  return (
    <header className="h-14 flex items-center justify-between px-6 bg-black/30 border-b border-gray-800 text-gray-200">
      <div className="flex items-center gap-4">
        <button className="p-2 rounded-md hover:bg-gray-800">?</button>
        <div className="text-sm font-medium">SENTINEL-AI Dashboard</div>
      </div>
      <div className="flex items-center gap-4 text-sm text-gray-400">
        <div>System Health: <span className="text-green-400">OK</span></div>
      </div>
    </header>
  )
}

export default TopNav

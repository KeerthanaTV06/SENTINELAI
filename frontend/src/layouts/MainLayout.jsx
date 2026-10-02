import React from 'react'
import Sidebar from '../components/Sidebar'
import TopNav from '../components/TopNav'

const Layout = ({ children }) => {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex-1 flex flex-col">
        <TopNav />
        <main className="p-6 overflow-auto bg-gradient-to-b from-black/40 via-gray-900 to-black">
          {children}
        </main>
      </div>
    </div>
  )
}

export default Layout

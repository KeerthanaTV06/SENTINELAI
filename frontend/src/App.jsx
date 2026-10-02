import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import DashboardPage from './pages/Dashboard'
import DatasetsPage from './pages/Datasets'
import ModelsPage from './pages/Models'
import PredictPage from './pages/Predict'
import ExplainPage from './pages/Explain'
import ReportsPage from './pages/Reports'
import Layout from './layouts/MainLayout'

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/datasets" element={<DatasetsPage />} />
        <Route path="/models" element={<ModelsPage />} />
        <Route path="/predict" element={<PredictPage />} />
        <Route path="/explain" element={<ExplainPage />} />
        <Route path="/reports" element={<ReportsPage />} />
      </Routes>
    </Layout>
  )
}

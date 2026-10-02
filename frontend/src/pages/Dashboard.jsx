import React, { useEffect, useState } from 'react'
import { listDatasets } from '../services/datasetService'
import { listModels } from '../services/modelService'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

const DashboardPage = () => {
  const [datasets, setDatasets] = useState([])
  const [models, setModels] = useState([])

  useEffect(() => {
    ;(async () => {
      try {
        const ds = await listDatasets()
        setDatasets(Array.isArray(ds.datasets) ? ds.datasets : Object.values(ds.datasets || {}))
      } catch (e) {
        console.error(e)
      }

      try {
        const ms = await listModels()
        setModels(ms.models || [])
      } catch (e) {
        console.error(e)
      }
    })()
  }, [])

  const datasetData = datasets.map((d) => ({
    name: d.name,
    value: 1,
  }))

  const modelData = (models || []).map((m) => ({
    name: m.name || m,
    accuracy: (m.metrics?.accuracy || 0) * 100,
  }))

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="p-4 bg-gray-800 rounded">Total Datasets: {datasets.length}</div>
        <div className="p-4 bg-gray-800 rounded">Models Available: {models.length}</div>
        <div className="p-4 bg-gray-800 rounded">Latest Accuracy: {modelData.length ? modelData[0].accuracy : 'N/A'}</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-4 bg-gray-800 rounded h-64">
          <h3 className="mb-2">Dataset Distribution</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={datasetData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#3b82f6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="p-4 bg-gray-800 rounded h-64">
          <h3 className="mb-2">Model Accuracy Comparison</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={modelData}>
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="accuracy" fill="#06b6d4" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default DashboardPage

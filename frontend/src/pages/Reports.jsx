import React, { useEffect, useState } from 'react'
import { listModels } from '../services/modelService'

const ReportsPage = () => {
  const [models, setModels] = useState([])

  useEffect(() => {
    loadModels()
  }, [])

  async function loadModels() {
    try {
      const res = await listModels()
      setModels(Array.isArray(res.models) ? res.models : Object.values(res.models || {}))
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">Reports</h2>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {models.map((model) => (
          <div key={model.model_name || model.name} className="bg-gray-800 rounded-lg p-5">
            <h3 className="text-xl font-semibold mb-4">{model.model_name || model.name}</h3>

            <p className="mb-2">
              <strong>Accuracy:</strong>{' '}
              {model.metrics?.accuracy != null ? (model.metrics.accuracy * 100).toFixed(2) + '%' : 'N/A'}
            </p>

            <p className="mb-4">
              <strong>Dataset:</strong>{' '}
              {model.metadata?.dataset || model.dataset || 'Unknown'}
            </p>

            <button
              className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
              onClick={() => alert('Evaluation reports will be downloadable in the next version.')}
            >
              View Report
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ReportsPage

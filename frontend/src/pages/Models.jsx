import React, { useEffect, useState } from 'react'
import { listModels, trainModel } from '../services/modelService'

const ModelsPage = () => {
  const [models, setModels] = useState([])
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchModels()
  }, [])

  async function fetchModels() {
    try {
      const ms = await listModels()
      setModels(Array.isArray(ms.models) ? ms.models : Object.values(ms.models || {}))
    } catch (e) {
      console.error('Models Error:', e)
    }
  }

  async function onTrain() {
    setLoading(true)

    try {
      await trainModel({
        model_name: 'random_forest',
        dataset_name: 'nslkdd',
        max_rows: 300,
      })

      await fetchModels()
    } catch (e) {
      console.error(e)
    }

    setLoading(false)
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">Models</h2>

        <button onClick={onTrain} className="px-4 py-2 bg-blue-600 rounded hover:bg-blue-700">
          {loading ? 'Training...' : 'Train Model'}
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {models.map((m) => (
          <div key={m.model_name || m.name} className="bg-gray-800 rounded-lg p-5 shadow">
            <h3 className="text-xl font-semibold mb-3">{m.model_name || m.name}</h3>

            <p className="text-gray-400 mb-2">
              <strong>Dataset:</strong>{' '}
              {m.metadata?.dataset || m.dataset || 'Unknown'}
            </p>

            <p className="text-gray-400 mb-2">
              <strong>Accuracy:</strong>{' '}
              {m.metrics?.accuracy != null ? (m.metrics.accuracy * 100).toFixed(2) + '%' : 'N/A'}
            </p>

            <p className="text-gray-400 mb-4"><strong>Status:</strong> Ready</p>

            <div className="flex gap-2">
              <button className="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600">Evaluate</button>
              <button className="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600">Explain</button>
              <button className="px-3 py-1 bg-gray-700 rounded hover:bg-gray-600">Predict</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ModelsPage

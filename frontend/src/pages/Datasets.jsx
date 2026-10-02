import React, { useEffect, useState } from 'react'
import { listDatasets, previewDataset } from '../services/datasetService'

const DatasetsPage = () => {
  const [datasets, setDatasets] = useState([])
  const [preview, setPreview] = useState([])

  useEffect(() => {
    ;(async () => {
      try {
        const ds = await listDatasets()
        setDatasets(Array.isArray(ds.datasets) ? ds.datasets : Object.values(ds.datasets || {}))
      } catch (e) {
        console.error('Dataset Error:', e)
      }
    })()
  }, [])

  const onPreview = async (name) => {
    try {
      const p = await previewDataset(name)
      setPreview(p.rows || [])
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">Datasets</h2>

      <div className="grid gap-4">
        {datasets.map((d) => (
          <div key={d.name} className="p-4 bg-gray-800 rounded flex justify-between items-center">
            <div>
              <h3 className="text-lg font-semibold">{d.display_name || d.name}</h3>
              <p className="text-gray-400 text-sm">{d.description}</p>
            </div>

            <button
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded"
              onClick={() => onPreview(d.name)}
            >
              Preview
            </button>
          </div>
        ))}
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-semibold mb-4">Dataset Preview</h3>
        <pre className="bg-gray-900 rounded p-4 overflow-auto max-h-96 text-xs">
          {JSON.stringify(preview, null, 2)}
        </pre>
      </div>
    </div>
  )
}

export default DatasetsPage

import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { predict } from '../services/modelService'

const PredictPage = () => {
  const { register, handleSubmit } = useForm()
  const [result, setResult] = useState(null)

  const onSubmit = async (data) => {
    try {
      const payload = { dataset_name: data.dataset_name || 'nslkdd', max_rows: 10 }
      const res = await predict(data.model_name || 'random_forest', payload)
      setResult(res)
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-4">Predict</h2>
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4 max-w-md">
        <div>
          <label className="block text-sm">Model Name</label>
          <input {...register('model_name')} className="w-full mt-1 p-2 bg-gray-800 rounded" defaultValue="random_forest" />
        </div>
        <div>
          <label className="block text-sm">Dataset</label>
          <input {...register('dataset_name')} className="w-full mt-1 p-2 bg-gray-800 rounded" defaultValue="nslkdd" />
        </div>
        <div>
          <button type="submit" className="px-4 py-2 bg-blue-600 rounded">Predict</button>
        </div>
      </form>

      {result && (
        <div className="mt-6">
          <h3 className="text-lg">Result</h3>
          <pre className="bg-gray-900 p-4 rounded max-h-64 overflow-auto text-xs">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default PredictPage

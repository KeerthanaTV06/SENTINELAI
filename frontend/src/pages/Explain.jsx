import React, { useState } from 'react'
import { useForm } from 'react-hook-form'
import { explain } from '../services/modelService'

const ExplainPage = () => {
  const { register, handleSubmit } = useForm()
  const [result, setResult] = useState(null)

  const onSubmit = async (data) => {
    try {
      const features = data.features.split(',').map((x) => Number(x.trim()))
      const featureNames = data.feature_names.split(',').map((x) => x.trim())

      const res = await explain(data.model_name || 'random_forest', {
        features,
        feature_names: featureNames,
      })

      setResult(res)
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div>
      <h2 className="text-2xl font-semibold mb-6">Explain Prediction</h2>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-5 max-w-4xl">
        <div>
          <label className="block mb-2">Model Name</label>
          <input {...register('model_name')} defaultValue="random_forest" className="w-full p-3 rounded bg-gray-800" />
        </div>

        <div>
          <label className="block mb-2">Feature Names</label>
          <textarea rows={3} {...register('feature_names')} defaultValue="duration,protocol_type,service,flag" className="w-full p-3 rounded bg-gray-800" />
        </div>

        <div>
          <label className="block mb-2">Feature Values</label>
          <textarea rows={3} {...register('features')} defaultValue="0,0,0,0" className="w-full p-3 rounded bg-gray-800" />
        </div>

        <button className="px-5 py-3 bg-blue-600 rounded hover:bg-blue-700">Explain</button>
      </form>

      {result && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-4">Explanation Result</h3>
          <pre className="bg-gray-900 rounded p-5 overflow-auto text-sm">{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  )
}

export default ExplainPage

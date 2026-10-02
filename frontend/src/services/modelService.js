import api from '../api/api'

export async function listModels() {
  const resp = await api.get('/api/v1/models')
  return resp.data
}

export async function trainModel(payload) {
  const resp = await api.post('/api/v1/models/train', payload)
  return resp.data
}

export async function predict(modelName, payload) {
  const resp = await api.post(`/api/v1/models/${modelName}/predict`, payload)
  return resp.data
}

export async function evaluate(modelName, payload) {
  const resp = await api.post(`/api/v1/models/${modelName}/evaluate`, payload)
  return resp.data
}

export async function explain(modelName, payload) {
  const resp = await api.post(`/api/v1/models/${modelName}/explain`, payload)
  return resp.data
}

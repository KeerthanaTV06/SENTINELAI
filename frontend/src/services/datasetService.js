import api from '../api/api'

export async function listDatasets() {
  const resp = await api.get('/api/v1/datasets')
  return resp.data
}

export async function previewDataset(name, rows = 5) {
  const resp = await api.get(`/api/v1/datasets/${name}/preview?rows=${rows}`)
  return resp.data
}

export async function datasetStats(name) {
  const resp = await api.get(`/api/v1/datasets/${name}/stats`)
  return resp.data
}

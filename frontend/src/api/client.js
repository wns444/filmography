import axios from 'axios'

const API_BASE = 'http://localhost:8000'

const client = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
    'accept': 'application/json',
  },
})

// Films API
export const filmsAPI = {
  getAll: (limit = 100, offset = 0) => 
    client.get('/api/v1/films/', { params: { limit, offset } }),
  getBySlug: (slug) => 
    client.get(`/api/v1/films/${slug}`),
  search: (query, limit = 100, offset = 0) =>
    client.get('/api/v1/films/', { params: { ...query, limit, offset } }),
}

// Serials API
export const serialsAPI = {
  getAll: (limit = 100, offset = 0) =>
    client.get('/api/v1/serials/', { params: { limit, offset } }),
  getBySlug: (slug) =>
    client.get(`/api/v1/serials/${slug}`),
  search: (query, limit = 100, offset = 0) =>
    client.get('/api/v1/serials/', { params: { ...query, limit, offset } }),
}

// Comments API
export const commentsAPI = {
  getFilmComments: (filmId) =>
    client.get(`/api/v1/films/${filmId}/comments`),
  getSerialComments: (serialId) =>
    client.get(`/api/v1/serials/${serialId}/comments`),
  addFilmComment: (filmId, comment) =>
    client.post(`/api/v1/films/${filmId}/comments`, comment),
}

export default client

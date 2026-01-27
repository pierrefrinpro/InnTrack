import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Clients
export const clientsAPI = {
  getAll: () => api.get('/clients/'),
  getOne: (id) => api.get(`/clients/${id}/`),
  create: (data) => api.post('/clients/', data),
  update: (id, data) => api.put(`/clients/${id}/`, data),
  delete: (id) => api.delete(`/clients/${id}/`),
};

// API Devis
export const devisAPI = {
  getAll: () => api.get('/devis/'),
  getOne: (id) => api.get(`/devis/${id}/`),
  create: (data) => api.post('/devis/', data),
  update: (id, data) => api.put(`/devis/${id}/`, data),
  delete: (id) => api.delete(`/devis/${id}/`),
};

// API Requêtes
export const requetesAPI = {
  getAll: () => api.get('/requetes/'),
  getOne: (id) => api.get(`/requetes/${id}/`),
  create: (data) => api.post('/requetes/', data),
  update: (id, data) => api.put(`/requetes/${id}/`, data),
  delete: (id) => api.delete(`/requetes/${id}/`),
};

// API Réalisations
export const realisationsAPI = {
  getAll: () => api.get('/realisations/'),
  getOne: (id) => api.get(`/realisations/${id}/`),
  create: (data) => api.post('/realisations/', data),
  update: (id, data) => api.put(`/realisations/${id}/`, data),
  delete: (id) => api.delete(`/realisations/${id}/`),
};

// API Factures
export const facturesAPI = {
  getAll: () => api.get('/factures/'),
  getOne: (id) => api.get(`/factures/${id}/`),
  create: (data) => api.post('/factures/', data),
  update: (id, data) => api.put(`/factures/${id}/`, data),
  delete: (id) => api.delete(`/factures/${id}/`),
};

export default api;

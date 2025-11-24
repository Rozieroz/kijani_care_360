import axios from 'axios'

const api = axios.create({
<<<<<<< HEAD
  baseURL: 'https://nonturbinated-latina-incongruently.ngrok-free.dev/api/v1',
=======
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
>>>>>>> 62c3b6f4805c95237a6acc48764a0ce4f87c4231
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
import axios from 'axios'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
})

http.interceptors.request.use(
  config => {
    const token = sessionStorage.getItem('token')
    if (token) {
      config.headers.token = token
    }
    return config
  },
  error => {
    return Promise.reject(error)
  },
)

export default http

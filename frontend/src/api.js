import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api'
})

// Tasks
export const getTasks = () => api.get('/tasks/')
export const createTask = (task) => api.post('/tasks/', task)
export const updateTask = (id, updates) => api.patch(`/tasks/${id}`, updates)
export const deleteTask = (id) => api.delete(`/tasks/${id}`)

// Schedule
export const getEvents = (date) => api.get('/schedule/events', { params: { date } })
export const createEvent = (event) => api.post('/schedule/events', event)
export const deleteEvent = (id) => api.delete(`/schedule/events/${id}`)
export const getFreeSlots = (date) => api.get(`/schedule/free-slots/${date}`)

// AI
export const estimateTask = (data) => api.post('/ai/estimate', data)
export const breakdownGoal = (data) => api.post('/ai/breakdown', data)
export const planDay = (date) => api.post('/ai/plan-day', { date })
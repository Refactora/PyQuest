import axios from 'axios'
import type {
  AuthResponse, Location, QuizStartResponse, AnswerResponse,
  QuizSessionState, BossStartResponse, BossSubmitResponse, HintResponse,
  ProfileResponse, LeaderboardResponse,
} from '../types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

// Автоматично додаємо токен до кожного запиту
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Якщо 401 — очищаємо токен (автологаут)
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

// ===== AUTH =====
export const authApi = {
  register: (data: { username: string; email: string; password: string; avatar_id: number }) =>
    api.post<AuthResponse>('/auth/register', data).then(r => r.data),

  login: (data: { email: string; password: string }) =>
    api.post<AuthResponse>('/auth/login', data).then(r => r.data),

  me: () => api.get<{ user: AuthResponse['user'] }>('/auth/me').then(r => r.data.user),
}

// ===== LOCATIONS =====
export const locationsApi = {
  getAll: () => api.get<{ locations: Location[]; total: number }>('/locations').then(r => r.data),
  getOne: (slug: string) => api.get<Location>(`/locations/${slug}`).then(r => r.data),
}

// ===== QUIZ =====
export const quizApi = {
  start: (location_slug: string) =>
    api.post<QuizStartResponse>('/quiz/start', { location_slug }).then(r => r.data),

  answer: (session_id: string, question_id: number, selected_option: string) =>
    api.post<AnswerResponse>('/quiz/answer', { session_id, question_id, selected_option }).then(r => r.data),

  getSession: (session_id: string) =>
    api.get<QuizSessionState>(`/quiz/session/${session_id}`).then(r => r.data),
}

// ===== BOSS =====
export const bossApi = {
  start: (location_slug: string) =>
    api.post<BossStartResponse>('/boss/start', { location_slug }).then(r => r.data),

  submit: (session_id: string, code: string) =>
    api.post<BossSubmitResponse>('/boss/submit', { session_id, code }).then(r => r.data),

  hint: (session_id: string, hint_order: number) =>
    api.post<HintResponse>('/boss/hint', { session_id, hint_order }).then(r => r.data),
}

// ===== PROFILE =====
export const profileApi = {
  get: () => api.get<ProfileResponse>('/profile').then(r => r.data),
  updateAvatar: (avatar_id: number) =>
    api.patch('/profile/avatar', { avatar_id }).then(r => r.data),
}

// ===== LEADERBOARD =====
export const leaderboardApi = {
  get: (limit = 50) =>
    api.get<LeaderboardResponse>(`/leaderboard?limit=${limit}`).then(r => r.data),
}

export default api

// ===== DAILY QUESTS =====
export const dailyQuestsApi = {
  get: () => api.get<import('../types').DailyQuestsResponse>('/daily-quests').then(r => r.data),
}

import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '../types'
import { authApi } from '../services/api'

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  error: string | null

  login: (email: string, password: string) => Promise<void>
  register: (data: { username: string; email: string; password: string; avatar_id: number }) => Promise<void>
  logout: () => void
  fetchMe: () => Promise<void>
  updateUser: (user: Partial<User>) => void
  clearError: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,
      error: null,

      login: async (email, password) => {
        set({ isLoading: true, error: null })
        try {
          const data = await authApi.login({ email, password })
          localStorage.setItem('token', data.access_token)
          set({ user: data.user, token: data.access_token, isLoading: false })
        } catch (err: any) {
          set({ error: err.response?.data?.detail || 'Помилка входу', isLoading: false })
          throw err
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null })
        try {
          const res = await authApi.register(data)
          localStorage.setItem('token', res.access_token)
          set({ user: res.user, token: res.access_token, isLoading: false })
        } catch (err: any) {
          set({ error: err.response?.data?.detail || 'Помилка реєстрації', isLoading: false })
          throw err
        }
      },

      logout: () => {
        localStorage.removeItem('token')
        set({ user: null, token: null })
      },

      fetchMe: async () => {
        const token = get().token || localStorage.getItem('token')
        if (!token) return
        try {
          const user = await authApi.me()
          set({ user })
        } catch {
          set({ user: null, token: null })
        }
      },

      updateUser: (updates) =>
        set((state) => ({ user: state.user ? { ...state.user, ...updates } : null })),

      clearError: () => set({ error: null }),
    }),
    {
      name: 'pyquest-auth',
      partialize: (state) => ({ token: state.token, user: state.user }),
    }
  )
)

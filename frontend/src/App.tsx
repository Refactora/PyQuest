import { useEffect } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useAuthStore } from './store/authStore'
import {
  LoginPage, RegisterPage, MapPage, LocationPage,
  ProfilePage, LeaderboardPage, AchievementsPage,
} from './pages'

function RequireAuth({ children }: { children: React.ReactNode }) {
  const { user, token, fetchMe } = useAuthStore()
  useEffect(() => { if (token && !user) fetchMe() }, [])
  if (!token) return <Navigate to="/login" replace />
  return <>{children}</>
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login"        element={<LoginPage />} />
        <Route path="/register"     element={<RegisterPage />} />
        <Route path="/map"          element={<RequireAuth><MapPage /></RequireAuth>} />
        <Route path="/location/:slug" element={<RequireAuth><LocationPage /></RequireAuth>} />
        <Route path="/profile"      element={<RequireAuth><ProfilePage /></RequireAuth>} />
        <Route path="/leaderboard"  element={<RequireAuth><LeaderboardPage /></RequireAuth>} />
        <Route path="/achievements" element={<RequireAuth><AchievementsPage /></RequireAuth>} />
        <Route path="/"             element={<Navigate to="/map" replace />} />
        <Route path="*"             element={<Navigate to="/map" replace />} />
      </Routes>
    </BrowserRouter>
  )
}

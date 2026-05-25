import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { XpBar } from '../ui'
import clsx from 'clsx'

const NAV_ITEMS = [
  { path: '/map', label: '🗺️ Карта', icon: '🗺️' },
  { path: '/leaderboard', label: '🏆 Лідери', icon: '🏆' },
  { path: '/profile', label: '⚔️ Профіль', icon: '⚔️' },
]

export function Navbar() {
  const { user, logout } = useAuthStore()
  const navigate = useNavigate()
  const location = useLocation()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  if (!user) return null

  return (
    <nav className="bg-gray-900 border-b border-gray-700 px-4 py-3 flex items-center justify-between sticky top-0 z-50">
      {/* Логотип */}
      <Link to="/map" className="text-yellow-400 font-bold text-xl flex items-center gap-2">
        <span>🐍</span>
        <span className="hidden sm:inline">PyQuest</span>
      </Link>

      {/* Навігація */}
      <div className="flex items-center gap-1">
        {NAV_ITEMS.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={clsx(
              'px-3 py-2 rounded-lg text-sm transition-colors',
              location.pathname.startsWith(item.path)
                ? 'bg-yellow-500 text-black font-bold'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
            )}
          >
            <span className="sm:hidden">{item.icon}</span>
            <span className="hidden sm:inline">{item.label}</span>
          </Link>
        ))}
      </div>

      {/* Юзер інфо */}
      <div className="flex items-center gap-3">
        {/* XP мінібар */}
        <div className="hidden md:block w-32">
          <XpBar current={user.xp} total={user.xp_to_next} level={user.level} />
        </div>

        {/* Стрік */}
        {user.streak_days > 0 && (
          <span className="text-orange-400 text-sm font-bold" title="Стрік">
            🔥{user.streak_days}
          </span>
        )}

        {/* Аватар + ім'я */}
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gray-700 flex items-center justify-center text-lg">
            {['🧙', '🦊', '🐉', '⚡'][user.avatar_id - 1] || '🧙'}
          </div>
          <span className="text-white text-sm font-medium hidden sm:inline">{user.username}</span>
        </div>

        <button
          onClick={handleLogout}
          className="text-gray-400 hover:text-red-400 text-sm transition-colors ml-1"
          title="Вийти"
        >
          🚪
        </button>
      </div>
    </nav>
  )
}

export function GameLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <Navbar />
      <main className="container mx-auto px-4 py-6 max-w-5xl">
        {children}
      </main>
    </div>
  )
}

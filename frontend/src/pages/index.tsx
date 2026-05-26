// ============================================================
// PAGES — всі сторінки PyQuest
// ============================================================
import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useAuthStore } from '../store/authStore'
import { useQuizStore, useBossStore } from '../store/gameStore'
import { locationsApi, quizApi, bossApi, profileApi, leaderboardApi } from '../services/api'
import { GameLayout } from '../components/layout/GameLayout'
import { LocationCard } from '../components/game/LocationCard'
import { QuizBattle } from '../components/game/QuizBattle'
import { BossFight } from '../components/game/BossFight'
import { HpBar, XpBar, Button, Card, Badge } from '../components/ui'
import type { Location, ProfileResponse, LeaderboardResponse } from '../types'

// ============================================================
// LOGIN PAGE
// ============================================================
const loginSchema = z.object({
  email: z.string().email('Невірний email'),
  password: z.string().min(1, 'Введіть пароль'),
})

export function LoginPage() {
  const { login, isLoading, error, clearError, user } = useAuthStore()
  const navigate = useNavigate()
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(loginSchema),
  })

  useEffect(() => { if (user) navigate('/map') }, [user])
  useEffect(() => { clearError() }, [])

  const onSubmit = async (data: any) => {
    try {
      await login(data.email, data.password)
      navigate('/map')
    } catch {}
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-6xl mb-3">🐍</div>
          <h1 className="text-3xl font-bold text-yellow-400">PyQuest</h1>
          <p className="text-gray-400 mt-1">Python RPG пригода</p>
        </div>

        <Card>
          <h2 className="text-white font-bold text-xl mb-5">Вхід до гри</h2>
          {error && (
            <div className="bg-red-900/40 border border-red-700 rounded-lg p-3 mb-4 text-red-300 text-sm">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <div>
              <label className="text-gray-400 text-sm block mb-1">Email</label>
              <input
                {...register('email')}
                type="email"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2.5 text-white focus:outline-none focus:border-yellow-500"
                placeholder="hero@pyquest.ua"
              />
              {errors.email && <p className="text-red-400 text-xs mt-1">{errors.email.message as string}</p>}
            </div>
            <div>
              <label className="text-gray-400 text-sm block mb-1">Пароль</label>
              <input
                {...register('password')}
                type="password"
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2.5 text-white focus:outline-none focus:border-yellow-500"
              />
              {errors.password && <p className="text-red-400 text-xs mt-1">{errors.password.message as string}</p>}
            </div>
            <Button type="submit" size="lg" className="w-full" loading={isLoading}>
              Увійти ⚔️
            </Button>
          </form>
          <p className="text-gray-500 text-sm text-center mt-4">
            Немає акаунту?{' '}
            <Link to="/register" className="text-yellow-400 hover:underline">Зареєструватись</Link>
          </p>
        </Card>
      </div>
    </div>
  )
}

// ============================================================
// REGISTER PAGE
// ============================================================
const registerSchema = z.object({
  username: z.string().min(3, 'Мінімум 3 символи').max(30),
  email: z.string().email('Невірний email'),
  password: z.string().min(6, 'Мінімум 6 символів'),
  avatar_id: z.number().min(1).max(4),
})

const AVATARS = [
  { id: 1, emoji: '🧙', name: 'Маг' },
  { id: 2, emoji: '🦊', name: 'Лис' },
  { id: 3, emoji: '🐉', name: 'Дракон' },
  { id: 4, emoji: '⚡', name: 'Блискавка' },
]

export function RegisterPage() {
  const { register: registerUser, isLoading, error, clearError } = useAuthStore()
  const navigate = useNavigate()
  const [selectedAvatar, setSelectedAvatar] = useState(1)
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: { avatar_id: 1 },
  })

  useEffect(() => { clearError() }, [])

  const onSubmit = async (data: any) => {
    try {
      await registerUser({ ...data, avatar_id: selectedAvatar })
      navigate('/map')
    } catch {}
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-6xl mb-3">🐍</div>
          <h1 className="text-3xl font-bold text-yellow-400">Створи героя</h1>
        </div>

        <Card>
          {error && (
            <div className="bg-red-900/40 border border-red-700 rounded-lg p-3 mb-4 text-red-300 text-sm">
              {error}
            </div>
          )}

          {/* Вибір аватара */}
          <div className="mb-5">
            <label className="text-gray-400 text-sm block mb-2">Обери персонажа</label>
            <div className="grid grid-cols-4 gap-2">
              {AVATARS.map((av) => (
                <button
                  key={av.id}
                  type="button"
                  onClick={() => setSelectedAvatar(av.id)}
                  className={`p-3 rounded-xl border-2 text-center transition-all ${
                    selectedAvatar === av.id
                      ? 'border-yellow-400 bg-yellow-900/30'
                      : 'border-gray-600 bg-gray-700 hover:border-gray-500'
                  }`}
                >
                  <div className="text-3xl">{av.emoji}</div>
                  <div className="text-xs text-gray-400 mt-1">{av.name}</div>
                </button>
              ))}
            </div>
          </div>

          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            {[
              { name: 'username', label: 'Ім\'я героя', type: 'text', placeholder: 'PythonHero' },
              { name: 'email', label: 'Email', type: 'email', placeholder: 'hero@pyquest.ua' },
              { name: 'password', label: 'Пароль', type: 'password', placeholder: '••••••' },
            ].map((field) => (
              <div key={field.name}>
                <label className="text-gray-400 text-sm block mb-1">{field.label}</label>
                <input
                  {...register(field.name as any)}
                  type={field.type}
                  placeholder={field.placeholder}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2.5 text-white focus:outline-none focus:border-yellow-500"
                />
                {errors[field.name as keyof typeof errors] && (
                  <p className="text-red-400 text-xs mt-1">
                    {errors[field.name as keyof typeof errors]?.message as string}
                  </p>
                )}
              </div>
            ))}

            <Button type="submit" size="lg" className="w-full" loading={isLoading}>
              Розпочати пригоду! 🐍
            </Button>
          </form>

          <p className="text-gray-500 text-sm text-center mt-4">
            Вже є акаунт?{' '}
            <Link to="/login" className="text-yellow-400 hover:underline">Увійти</Link>
          </p>
        </Card>
      </div>
    </div>
  )
}

// ============================================================
// MAP PAGE
// ============================================================
export function MapPage() {
  const { user } = useAuthStore()
  const [locations, setLocations] = useState<Location[]>([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    locationsApi.getAll()
      .then(r => setLocations(r.locations))
      .finally(() => setIsLoading(false))
  }, [])

  const completed = locations.filter(l => l.progress.boss_defeated).length

  return (
    <GameLayout>
      {/* Hero stats */}
      {user && (
        <div className="mb-6">
          <Card>
            <div className="flex items-center gap-4 flex-wrap">
              <div className="text-4xl">
                {['🧙', '🦊', '🐉', '⚡'][user.avatar_id - 1]}
              </div>
              <div className="flex-1 min-w-48">
                <div className="flex items-center gap-3 mb-2">
                  <h2 className="text-white font-bold text-xl">{user.username}</h2>
                  <Badge variant="warning">Рівень {user.level}</Badge>
                  {user.streak_days > 1 && <Badge variant="danger">🔥 {user.streak_days} днів</Badge>}
                </div>
                <XpBar current={user.xp} total={user.xp_to_next} level={user.level} />
              </div>
              <div className="text-right">
                <p className="text-gray-400 text-sm">Прогрес</p>
                <p className="text-2xl font-bold text-yellow-400">{completed}/10</p>
                <p className="text-gray-500 text-xs">локацій</p>
              </div>
            </div>
          </Card>
        </div>
      )}

      <h2 className="text-white font-bold text-2xl mb-4">🗺️ Карта Пригод</h2>

      {isLoading ? (
        <div className="text-center py-20 text-gray-400">Завантаження карти...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {locations.map((loc, i) => (
            <LocationCard key={loc.id} location={loc} index={i} />
          ))}
        </div>
      )}
    </GameLayout>
  )
}

// ============================================================
// LOCATION DETAIL PAGE
// ============================================================
export function LocationPage() {
  const { slug } = useParams<{ slug: string }>()
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const quizStore = useQuizStore()
  const bossStore = useBossStore()
  const [location, setLocation] = useState<Location | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [view, setView] = useState<'info' | 'quiz' | 'boss'>('info')
  const [quizFinishResult, setQuizFinishResult] = useState<any>(null)

  useEffect(() => {
    if (!slug) return
    locationsApi.getOne(slug)
      .then(setLocation)
      .finally(() => setIsLoading(false))
  }, [slug])

  if (isLoading) return <GameLayout><div className="text-center py-20 text-gray-400">Завантаження...</div></GameLayout>
  if (!location) return <GameLayout><div className="text-center py-20 text-red-400">Локацію не знайдено</div></GameLayout>

  // СТАРТ КВІЗУ
  const handleStartQuiz = async () => {
    try {
      const res = await quizApi.start(location.slug)
      quizStore.setSession({
        sessionId: res.session_id,
        locationSlug: location.slug,
        locationName: location.name,
        heroHp: res.hero_hp,
        maxHp: user?.hp_max ?? 5,
        question: res.question,
        questionNumber: res.question_number,
        totalQuestions: res.total_questions,
      })
      setView('quiz')
    } catch (err: any) {
      alert(err.response?.data?.detail ?? 'Помилка старту квізу')
    }
  }

  // СТАРТ БОСУ
  const handleStartBoss = async () => {
    try {
      const res = await bossApi.start(location.slug)
      bossStore.setSession(res, user?.hp_max ?? 5)
      setView('boss')
    } catch (err: any) {
      alert(err.response?.data?.detail ?? 'Помилка старту боса')
    }
  }

  const handleQuizFinish = (result: any) => {
    setQuizFinishResult(result)
    setView('info')
    // Оновити локацію
    locationsApi.getOne(slug!).then(setLocation)
  }

  const handleBossWin = (xpGained: number, achievements: string[]) => {
    setView('info')
    bossStore.reset()
    locationsApi.getOne(slug!).then(setLocation)
  }

  const handleBossLose = () => {
    setView('info')
    bossStore.reset()
  }

  return (
    <GameLayout>
      {view === 'quiz' && (
        <div>
          <div className="flex items-center gap-3 mb-6">
            <button onClick={() => { setView('info'); quizStore.reset() }} className="text-gray-400 hover:text-white">← Назад</button>
            <h1 className="text-xl font-bold text-white">{location.name} — Квіз</h1>
          </div>
          <QuizBattle onFinish={handleQuizFinish} />
        </div>
      )}

      {view === 'boss' && (
        <div>
          <div className="flex items-center gap-3 mb-6">
            <button onClick={() => { setView('info'); bossStore.reset() }} className="text-gray-400 hover:text-white">← Назад</button>
            <h1 className="text-xl font-bold text-white">{location.name} — Бій з Босом</h1>
          </div>
          <BossFight onWin={handleBossWin} onLose={handleBossLose} />
        </div>
      )}

      {view === 'info' && (
        <div className="space-y-5">
          <div className="flex items-center gap-3">
            <button onClick={() => navigate('/map')} className="text-gray-400 hover:text-white text-sm">← Карта</button>
            <h1 className="text-2xl font-bold text-white" style={{ color: location.color_theme }}>
              {location.name}
            </h1>
          </div>

          {/* Результат квізу */}
          {quizFinishResult && (
            <Card className="border-l-4 border-l-green-500">
              <h3 className="text-green-400 font-bold mb-1">✅ Квіз завершено!</h3>
              <p className="text-gray-300 text-sm">
                Результат: {quizFinishResult.score}/10
                {quizFinishResult.noDeathRun && ' 🛡️ Без смертей!'}
                {quizFinishResult.perfectScore && ' ⭐ Ідеально!'}
              </p>
              <p className="text-gray-400 text-sm mt-1">Тепер можеш боротися з босом!</p>
            </Card>
          )}

          {/* Опис локації */}
          <Card>
            <p className="text-gray-300">{location.description}</p>
            <p className="text-yellow-400 text-sm mt-2 font-medium">🎓 Тема: {location.topic}</p>
          </Card>

          {/* Кнопки дій */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {/* Квіз */}
            <Card className="flex flex-col gap-3">
              <div>
                <h3 className="text-white font-bold">⚔️ Квіз — Битва з крипами</h3>
                <p className="text-gray-400 text-sm mt-1">10 питань. Відповідай вірно — вбивай крипів!</p>
                {location.progress.best_quiz_score > 0 && (
                  <Badge variant="success" className="mt-2">
                    Кращий результат: {location.progress.best_quiz_score}/10
                  </Badge>
                )}
              </div>
              <Button
                onClick={handleStartQuiz}
                disabled={location.progress.status === 'locked'}
              >
                {location.progress.quiz_completed ? '🔄 Пройти знову' : '▶️ Почати квіз'}
              </Button>
            </Card>

            {/* Бос */}
            <Card className={`flex flex-col gap-3 ${!location.progress.quiz_completed ? 'opacity-60' : ''}`}>
              <div>
                <h3 className="text-white font-bold">👹 Бос — {location.boss_name}</h3>
                <p className="text-gray-400 text-sm mt-1">Вирішуй задачу щоб завдати шкоди босу!</p>
                {location.progress.boss_defeated && (
                  <Badge variant="success" className="mt-2">Переможено!</Badge>
                )}
                {!location.progress.quiz_completed && (
                  <p className="text-red-400 text-xs mt-1">🔒 Спочатку пройди квіз</p>
                )}
              </div>
              <Button
                onClick={handleStartBoss}
                variant={location.progress.boss_defeated ? 'secondary' : 'primary'}
                disabled={!location.progress.quiz_completed}
              >
                {location.progress.boss_defeated ? '🔄 Бій знову' : '⚡ Боротися з босом'}
              </Button>
            </Card>
          </div>
        </div>
      )}
    </GameLayout>
  )
}

// ============================================================
// PROFILE PAGE
// ============================================================
export function ProfilePage() {
  const { user, updateUser } = useAuthStore()
  const [profile, setProfile] = useState<ProfileResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    profileApi.get()
      .then(setProfile)
      .finally(() => setIsLoading(false))
  }, [])

  const handleAvatarChange = async (avatarId: number) => {
    await profileApi.updateAvatar(avatarId)
    updateUser({ avatar_id: avatarId })
    setProfile(p => p ? { ...p, avatar_id: avatarId } : p)
  }

  if (isLoading) return <GameLayout><div className="text-center py-20 text-gray-400">Завантаження...</div></GameLayout>
  if (!profile) return <GameLayout><div className="text-center py-20 text-red-400">Помилка</div></GameLayout>

  const AVATARS = [
    { id: 1, emoji: '🧙' }, { id: 2, emoji: '🦊' },
    { id: 3, emoji: '🐉' }, { id: 4, emoji: '⚡' },
  ]

  return (
    <GameLayout>
      <div className="space-y-5 max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-white">⚔️ Профіль Героя</h1>

        {/* Головна картка */}
        <Card>
          <div className="flex items-center gap-5">
            <div className="text-6xl">{AVATARS.find(a => a.id === profile.avatar_id)?.emoji ?? '🧙'}</div>
            <div className="flex-1">
              <h2 className="text-2xl font-bold text-white">{profile.username}</h2>
              <p className="text-yellow-400 text-sm">{profile.title}</p>
              <div className="mt-2">
                <XpBar current={profile.xp} total={profile.xp_to_next} level={profile.level} />
              </div>
            </div>
          </div>

          {/* Зміна аватара */}
          <div className="mt-4 pt-4 border-t border-gray-700">
            <p className="text-gray-400 text-sm mb-2">Змінити аватар:</p>
            <div className="flex gap-2">
              {AVATARS.map(av => (
                <button
                  key={av.id}
                  onClick={() => handleAvatarChange(av.id)}
                  className={`p-2 rounded-lg border-2 text-2xl transition-all ${
                    profile.avatar_id === av.id ? 'border-yellow-400 bg-yellow-900/30' : 'border-gray-600 hover:border-gray-400'
                  }`}
                >
                  {av.emoji}
                </button>
              ))}
            </div>
          </div>
        </Card>

        {/* Статистика */}
        <div className="grid grid-cols-3 gap-3">
          {[
            { label: 'Локацій', value: profile.stats.locations_completed, emoji: '🗺️' },
            { label: 'Квізів', value: profile.stats.total_quiz_attempts, emoji: '❓' },
            { label: 'Стрік', value: `${profile.streak_days} 🔥`, emoji: '' },
          ].map((stat) => (
            <Card key={stat.label} className="text-center">
              <div className="text-2xl font-bold text-yellow-400">{stat.emoji} {stat.value}</div>
              <div className="text-gray-400 text-sm">{stat.label}</div>
            </Card>
          ))}
        </div>

        {/* Ачівменти */}
        {profile.achievements.length > 0 && (
          <Card>
            <h3 className="text-white font-bold mb-3">🏅 Досягнення ({profile.achievements.length})</h3>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {profile.achievements.map(ach => (
                <div key={ach.id} className="bg-gray-700 rounded-lg p-3 flex items-center gap-3">
                  <span className="text-2xl">🏅</span>
                  <div>
                    <p className="text-white text-sm font-medium">{ach.name}</p>
                    <p className="text-gray-400 text-xs">{ach.description}</p>
                    {ach.xp_reward > 0 && <Badge variant="warning">+{ach.xp_reward} XP</Badge>}
                  </div>
                </div>
              ))}
            </div>
          </Card>
        )}
      </div>
    </GameLayout>
  )
}

// ============================================================
// LEADERBOARD PAGE
// ============================================================
export function LeaderboardPage() {
  const [data, setData] = useState<LeaderboardResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    leaderboardApi.get(50).then(setData).finally(() => setIsLoading(false))
  }, [])

  const RANK_MEDALS: Record<number, string> = { 1: '🥇', 2: '🥈', 3: '🥉' }
  const AV = ['🧙', '🦊', '🐉', '⚡']

  return (
    <GameLayout>
      <div className="max-w-2xl mx-auto">
        <h1 className="text-2xl font-bold text-white mb-2">🏆 Лідери PyQuest</h1>
        {data && (
          <p className="text-gray-400 text-sm mb-5">Всього гравців: {data.total_players}</p>
        )}

        {isLoading ? (
          <div className="text-center py-20 text-gray-400">Завантаження...</div>
        ) : data ? (
          <div className="space-y-2">
            {/* Моя позиція якщо не в топі */}
            {data.my_entry && data.my_rank && data.my_rank > 50 && (
              <Card className="border-yellow-700 bg-yellow-900/20 mb-4">
                <p className="text-yellow-400 text-sm mb-1">Твоя позиція:</p>
                <LeaderboardRow entry={data.my_entry} medals={RANK_MEDALS} avatars={AV} />
              </Card>
            )}

            {data.leaderboard.map((entry) => (
              <div
                key={entry.user_id}
                className={entry.is_me ? 'ring-2 ring-yellow-500 rounded-xl' : ''}
              >
                <Card className={entry.is_me ? 'bg-yellow-900/20' : ''}>
                  <LeaderboardRow entry={entry} medals={RANK_MEDALS} avatars={AV} />
                </Card>
              </div>
            ))}
          </div>
        ) : null}
      </div>
    </GameLayout>
  )
}

function LeaderboardRow({ entry, medals, avatars }: {
  entry: any; medals: Record<number, string>; avatars: string[]
}) {
  return (
    <div className="flex items-center gap-3">
      <span className="text-xl w-8 text-center">{medals[entry.rank] ?? `#${entry.rank}`}</span>
      <span className="text-2xl">{avatars[entry.avatar_id - 1] ?? '🧙'}</span>
      <div className="flex-1 min-w-0">
        <p className="text-white font-medium truncate">
          {entry.username}
          {entry.is_me && <Badge variant="warning" className="ml-2">Ти</Badge>}
        </p>
        <p className="text-gray-400 text-xs">{entry.title}</p>
      </div>
      <div className="text-right">
        <p className="text-yellow-400 font-bold">{entry.total_xp.toLocaleString()} XP</p>
        <p className="text-gray-500 text-xs">Рівень {entry.level}</p>
      </div>
    </div>
  )
}

// ============================================================
// ACHIEVEMENTS PAGE
// ============================================================
export function AchievementsPage() {
  const [profile, setProfile] = useState<ProfileResponse | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    profileApi.get().then(setProfile).finally(() => setIsLoading(false))
  }, [])

  const ALL_ACHIEVEMENTS = [
    { slug: 'first_blood',   name: 'Перший Крип',       description: 'Дай першу правильну відповідь',        icon: '⚔️',  xp: 10  },
    { slug: 'no_death_1',    name: 'Безсмертний',         description: 'Пройди квіз без жодної смерті',        icon: '🛡️',  xp: 25  },
    { slug: 'boss_slayer',   name: 'Переможець Босів',    description: 'Вбий першого боса',                    icon: '💀',  xp: 50  },
    { slug: 'all_bosses',    name: 'Кілер Босів',         description: 'Вбий всіх 10 босів',                   icon: '👑',  xp: 200 },
    { slug: 'perfectionist', name: 'Перфекціоніст',       description: '10/10 у квізі без помилок',            icon: '⭐',  xp: 30  },
    { slug: 'first_try',     name: 'З Першої Спроби',     description: 'Вбий боса з першої спроби',            icon: '⚡',  xp: 50  },
    { slug: 'no_hints',      name: 'Без Підказок',        description: 'Вбий боса без підказок',               icon: '🧠',  xp: 30  },
    { slug: 'streak_3',      name: 'На Роботі',           description: '3 дні стріку поспіль',                 icon: '🔥',  xp: 30  },
    { slug: 'streak_7',      name: 'Тижневий Герой',      description: 'Стрік 7 днів',                         icon: '🔥',  xp: 100 },
    { slug: 'streak_30',     name: 'Місячний Герой',      description: 'Стрік 30 днів',                        icon: '🔥',  xp: 500 },
    { slug: 'speed_run',     name: 'Спідранер',           description: 'Пройди локацію менш ніж за 5 хвилин',  icon: '⏱️',  xp: 75  },
    { slug: 'completionist', name: 'Завершувач',          description: 'Пройди всі 10 локацій',                icon: '🏆',  xp: 300 },
    { slug: 'level_10',      name: 'Досвідчений',         description: 'Досягни 10 рівня',                     icon: '💎',  xp: 50  },
    { slug: 'level_20',      name: 'Ветеран',             description: 'Досягни 20 рівня',                     icon: '💎',  xp: 100 },
  ]

  const unlockedSlugs = new Set(profile?.achievements.map(a => a.slug) ?? [])
  const unlocked = ALL_ACHIEVEMENTS.filter(a => unlockedSlugs.has(a.slug))
  const locked = ALL_ACHIEVEMENTS.filter(a => !unlockedSlugs.has(a.slug))

  return (
    <GameLayout>
      <div className="max-w-3xl mx-auto">
        <h1 className="text-2xl font-bold text-white mb-1">🏅 Досягнення</h1>
        {profile && (
          <p className="text-gray-400 text-sm mb-5">
            Розблоковано: {unlocked.length} / {ALL_ACHIEVEMENTS.length}
          </p>
        )}

        {isLoading ? (
          <div className="text-center py-20 text-gray-400">Завантаження...</div>
        ) : (
          <div className="space-y-6">
            {unlocked.length > 0 && (
              <div>
                <h2 className="text-green-400 font-semibold mb-3">✅ Отримані</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {unlocked.map(a => (
                    <div key={a.slug} className="bg-gray-800 border border-green-700/40 rounded-xl p-4 flex items-center gap-3">
                      <span className="text-3xl">{a.icon}</span>
                      <div>
                        <p className="text-white font-medium">{a.name}</p>
                        <p className="text-gray-400 text-xs">{a.description}</p>
                        <p className="text-yellow-400 text-xs mt-1">+{a.xp} XP</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {locked.length > 0 && (
              <div>
                <h2 className="text-gray-500 font-semibold mb-3">🔒 Заблоковані</h2>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  {locked.map(a => (
                    <div key={a.slug} className="bg-gray-900 border border-gray-700 rounded-xl p-4 flex items-center gap-3 opacity-50">
                      <span className="text-3xl grayscale">{a.icon}</span>
                      <div>
                        <p className="text-gray-400 font-medium">{a.name}</p>
                        <p className="text-gray-600 text-xs">{a.description}</p>
                        <p className="text-gray-600 text-xs mt-1">+{a.xp} XP</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </GameLayout>
  )
}

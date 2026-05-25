import { useNavigate } from 'react-router-dom'
import clsx from 'clsx'
import type { Location } from '../../types'
import { Badge } from '../ui'

const STATUS_LABEL: Record<string, string> = {
  locked: '🔒 Заблоковано',
  available: '✨ Доступно',
  in_progress: '⚔️ В процесі',
  completed: '✅ Завершено',
}

const AVATARS = ['🌱', '⚔️', '🔮', '🐉', '🌊', '🏰', '☁️', '💀', '🏛️', '🗼']

interface LocationCardProps {
  location: Location
  index: number
}

export function LocationCard({ location, index }: LocationCardProps) {
  const navigate = useNavigate()
  const { progress } = location
  const isLocked = progress.status === 'locked'
  const isCompleted = progress.status === 'completed'

  const handleClick = () => {
    if (!isLocked) navigate(`/location/${location.slug}`)
  }

  return (
    <div
      onClick={handleClick}
      className={clsx(
        'relative rounded-xl border p-5 transition-all duration-300',
        isLocked
          ? 'border-gray-700 bg-gray-900 opacity-60 cursor-not-allowed'
          : 'border-gray-600 bg-gray-800 cursor-pointer hover:border-yellow-500 hover:shadow-lg hover:shadow-yellow-900/20 hover:-translate-y-0.5'
      )}
      style={!isLocked ? { borderLeftColor: location.color_theme, borderLeftWidth: 4 } : undefined}
    >
      {/* Номер + іконка */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{AVATARS[index] || '⚡'}</span>
          <div>
            <p className="text-xs text-gray-500">Локація {location.order_index}</p>
            <h3 className="font-bold text-white text-lg leading-tight">{location.name}</h3>
          </div>
        </div>

        {/* Статус */}
        <Badge
          variant={
            isCompleted ? 'success'
              : progress.status === 'available' ? 'info'
              : progress.status === 'in_progress' ? 'warning'
              : 'default'
          }
        >
          {STATUS_LABEL[progress.status]}
        </Badge>
      </div>

      {/* Тема */}
      <p className="text-gray-400 text-sm mb-3">{location.topic}</p>

      {/* Прогрес бар квізу та босу */}
      {!isLocked && (
        <div className="flex gap-3 mt-3">
          <div className={clsx(
            'flex-1 text-center py-1.5 rounded-lg text-xs font-medium border',
            progress.quiz_completed
              ? 'bg-green-900/40 border-green-700 text-green-400'
              : 'bg-gray-700 border-gray-600 text-gray-400'
          )}>
            {progress.quiz_completed ? '✅ Квіз пройдено' : '❓ Квіз'}
            {progress.best_quiz_score > 0 && (
              <span className="ml-1 text-gray-500">({progress.best_quiz_score}/10)</span>
            )}
          </div>

          <div className={clsx(
            'flex-1 text-center py-1.5 rounded-lg text-xs font-medium border',
            progress.boss_defeated
              ? 'bg-purple-900/40 border-purple-700 text-purple-400'
              : 'bg-gray-700 border-gray-600 text-gray-400'
          )}>
            {progress.boss_defeated ? `✅ ${location.boss_name}` : `👹 ${location.boss_name}`}
          </div>
        </div>
      )}

      {/* Бонуси */}
      {isCompleted && (
        <div className="flex gap-2 mt-2 flex-wrap">
          {progress.first_try_boss && <Badge variant="warning">⚡ З першої спроби</Badge>}
          {progress.no_death_run && <Badge variant="info">🛡️ Без смертей</Badge>}
        </div>
      )}

      {/* Замок оверлей */}
      {isLocked && (
        <div className="absolute inset-0 flex items-center justify-center">
          <span className="text-4xl opacity-30">🔒</span>
        </div>
      )}
    </div>
  )
}

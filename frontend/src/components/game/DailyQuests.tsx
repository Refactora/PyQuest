import { useEffect, useState } from 'react'
import { dailyQuestsApi } from '../../services/api'
import type { DailyQuestsResponse } from '../../types'
import clsx from 'clsx'

export function DailyQuestsPanel() {
  const [data, setData] = useState<DailyQuestsResponse | null>(null)
  const [open, setOpen] = useState(false)

  useEffect(() => {
    dailyQuestsApi.get().then(setData).catch(() => {})
  }, [])

  if (!data) return null

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className={clsx(
          'flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors',
          data.all_done ? 'bg-green-900/60 text-green-300' : 'bg-gray-800 text-gray-300 hover:bg-gray-700'
        )}
      >
        <span>📋</span>
        <span className="hidden sm:inline">Квести</span>
        <span className={clsx(
          'px-1.5 py-0.5 rounded text-xs font-bold',
          data.all_done ? 'bg-green-500 text-black' : 'bg-yellow-500 text-black'
        )}>
          {data.completed}/{data.total}
        </span>
      </button>

      {open && (
        <div className="absolute right-0 top-full mt-2 w-72 bg-gray-900 border border-gray-700 rounded-xl shadow-2xl z-50 p-4">
          <h3 className="text-white font-bold mb-3 flex items-center gap-2">
            📋 Щоденні квести
            {data.all_done && <span className="text-green-400 text-sm">✅ Всі виконані!</span>}
          </h3>
          <div className="space-y-3">
            {data.quests.map(q => (
              <div key={q.id} className={clsx(
                'rounded-lg p-3 border',
                q.is_completed ? 'bg-green-900/30 border-green-700' : 'bg-gray-800 border-gray-700'
              )}>
                <div className="flex items-start justify-between gap-2">
                  <p className={clsx('text-sm', q.is_completed ? 'text-green-300 line-through' : 'text-gray-200')}>
                    {q.description}
                  </p>
                  <span className="text-yellow-400 text-xs font-bold whitespace-nowrap">
                    +{q.xp_reward} XP
                  </span>
                </div>
                {!q.is_completed && (
                  <div className="mt-2">
                    <div className="flex justify-between text-xs text-gray-500 mb-1">
                      <span>{q.current_value}/{q.target_value}</span>
                      <span>{q.progress_pct}%</span>
                    </div>
                    <div className="h-1.5 bg-gray-700 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-blue-500 rounded-full transition-all"
                        style={{ width: `${q.progress_pct}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

import { useState, useRef } from 'react'
import Editor from '@monaco-editor/react'
import clsx from 'clsx'
import { useBossStore } from '../../store/gameStore'
import { bossApi } from '../../services/api'
import { HpBar, BossHpBar, Button, Card, Badge } from '../ui'
import type { TestResult } from '../../types'

interface BossFightProps {
  onWin: (xpGained: number, achievements: string[]) => void
  onLose: () => void
}

export function BossFight({ onWin, onLose }: BossFightProps) {
  const store = useBossStore()
  const [code, setCode] = useState(store.challengeData?.starter_code ?? '')
  const [activeTab, setActiveTab] = useState<'task' | 'tests' | 'results'>('task')

  const { sessionId, bossData, challengeData, heroHp, maxHp, bossHp, maxBossHp,
    hintsAvailable, hintsUsed, testResults, lastSubmit, currentHint, isWon, isLost } = store

  if (!bossData || !challengeData) return null

  const handleSubmit = async () => {
    if (!sessionId || store.isSubmitting) return
    store.setSubmitting(true)
    try {
      const res = await bossApi.submit(sessionId, code)
      store.setSubmitResult(res)
      setActiveTab('results')

      if (res.is_won) {
        setTimeout(() => onWin(res.xp_gained ?? 0, res.new_achievements ?? []), 2000)
      }
      if (res.hero_died) {
        setTimeout(() => onLose(), 2000)
      }
    } finally {
      store.setSubmitting(false)
    }
  }

  const handleHint = async (order: number) => {
    if (!sessionId || order <= hintsUsed) return
    try {
      const res = await bossApi.hint(sessionId, order)
      store.setHint(res.hint_text, res.hints_used, res.hero_hp, res.hero_died)
      if (res.hero_died) setTimeout(() => onLose(), 1500)
    } catch (err: any) {
      alert(err.response?.data?.detail ?? 'Помилка')
    }
  }

  return (
    <div className="space-y-4">
      {/* HUD */}
      <div className="grid grid-cols-2 gap-4">
        <HpBar current={heroHp} max={maxHp} label="❤️ HP Героя" />
        <BossHpBar current={bossHp} max={maxBossHp} bossName={bossData.name} />
      </div>

      {/* Результат */}
      {lastSubmit && (
        <div className={clsx(
          'rounded-xl p-3 border text-sm font-medium',
          lastSubmit.is_won
            ? 'bg-green-900/40 border-green-600 text-green-300'
            : lastSubmit.hero_died
            ? 'bg-red-900/40 border-red-600 text-red-300'
            : 'bg-gray-800 border-gray-600 text-gray-300'
        )}>
          {lastSubmit.is_won
            ? `🏆 БОС ПЕРЕМОЖЕНИЙ! +${lastSubmit.xp_gained} XP`
            : lastSubmit.hero_died
            ? '💀 Бос переміг! Твій герой загинув...'
            : `⚔️ Спроба #${store.attemptNumber}: ${lastSubmit.passed_count}/${lastSubmit.total_count} тестів пройдено`}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Ліва панель — умова + підказки + тести */}
        <div className="space-y-3">
          {/* Таби */}
          <div className="flex rounded-lg overflow-hidden border border-gray-700">
            {(['task', 'tests', 'results'] as const).map((tab) => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={clsx(
                  'flex-1 py-2 text-sm transition-colors',
                  activeTab === tab
                    ? 'bg-yellow-500 text-black font-bold'
                    : 'bg-gray-800 text-gray-400 hover:text-white'
                )}
              >
                {tab === 'task' ? '📜 Умова' : tab === 'tests' ? '🧪 Тести' : '📊 Результати'}
              </button>
            ))}
          </div>

          <Card className="max-h-72 overflow-y-auto">
            {activeTab === 'task' && (
              <div className="space-y-3">
                <h3 className="text-yellow-400 font-bold">{challengeData.title}</h3>
                <p className="text-gray-400 text-sm italic">{challengeData.story_text}</p>
                <div className="border-t border-gray-700 pt-3">
                  <pre className="text-gray-200 text-sm whitespace-pre-wrap font-mono leading-relaxed">
                    {challengeData.task_text}
                  </pre>
                </div>
              </div>
            )}

            {activeTab === 'tests' && (
              <div className="space-y-2">
                <p className="text-gray-400 text-xs mb-3">Відкриті тест-кейси:</p>
                {challengeData.visible_test_cases.map((tc, i) => (
                  <div key={i} className="bg-gray-900 rounded-lg p-3 text-xs font-mono">
                    <p className="text-gray-500"># {tc.description}</p>
                    <p><span className="text-blue-400">вхід:</span> <span className="text-white">{tc.input}</span></p>
                    <p><span className="text-green-400">очікується:</span> <span className="text-white">{tc.expected_output}</span></p>
                  </div>
                ))}
              </div>
            )}

            {activeTab === 'results' && (
              <div className="space-y-2">
                {testResults.length === 0
                  ? <p className="text-gray-500 text-sm">Ще немає результатів. Відправ код!</p>
                  : testResults.map((tr, i) => <TestResultRow key={i} result={tr} index={i} />)}
              </div>
            )}
          </Card>

          {/* Підказки */}
          <Card>
            <p className="text-gray-400 text-xs mb-2">💡 Підказки (коштують HP):</p>
            <div className="flex gap-2 flex-wrap">
              {[1, 2, 3].slice(0, hintsAvailable).map((order) => {
                const used = order <= hintsUsed
                return (
                  <button
                    key={order}
                    onClick={() => handleHint(order)}
                    disabled={used}
                    className={clsx(
                      'px-3 py-1.5 rounded-lg text-xs border transition-colors',
                      used
                        ? 'border-gray-700 bg-gray-800 text-gray-600 cursor-not-allowed'
                        : 'border-yellow-700 bg-yellow-900/30 text-yellow-400 hover:bg-yellow-900/60'
                    )}
                  >
                    {used ? `✅ Підказка ${order}` : `💡 Підказка ${order} (-${order === 1 ? 10 : order === 2 ? 10 : 15} HP)`}
                  </button>
                )
              })}
            </div>

            {currentHint && (
              <div className="mt-3 bg-yellow-900/20 border border-yellow-700 rounded-lg p-3">
                <p className="text-yellow-300 text-sm">{currentHint}</p>
              </div>
            )}
          </Card>
        </div>

        {/* Права панель — редактор */}
        <div className="space-y-3">
          <div className="rounded-xl overflow-hidden border border-gray-700 h-72">
            <div className="bg-gray-800 px-3 py-1.5 border-b border-gray-700 flex items-center justify-between">
              <span className="text-gray-400 text-xs font-mono">solution.py</span>
              <Badge variant="info">Python 3</Badge>
            </div>
            <Editor
              height="100%"
              language="python"
              theme="vs-dark"
              value={code}
              onChange={(v) => setCode(v ?? '')}
              options={{
                fontSize: 14,
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                padding: { top: 12 },
                lineNumbers: 'on',
                tabSize: 4,
              }}
            />
          </div>

          <Button
            size="lg"
            className="w-full"
            onClick={handleSubmit}
            loading={store.isSubmitting}
            disabled={isWon || isLost}
          >
            {store.isSubmitting ? 'Виконую тести...' : '🚀 Запустити рішення'}
          </Button>

          <p className="text-gray-600 text-xs text-center">
            os, sys, subprocess та мережеві виклики заборонені
          </p>
        </div>
      </div>
    </div>
  )
}

function TestResultRow({ result, index }: { result: TestResult; index: number }) {
  return (
    <div className={clsx(
      'rounded-lg p-3 text-xs border',
      result.passed ? 'bg-green-900/30 border-green-700' : 'bg-red-900/30 border-red-700'
    )}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-gray-400">
          {result.is_hidden ? `🔒 Прихований тест ${index + 1}` : result.description || `Тест ${index + 1}`}
        </span>
        <span>{result.passed ? '✅ Пройдено' : '❌ Провалено'}</span>
      </div>
      {!result.is_hidden && (
        <div className="font-mono space-y-0.5">
          {result.actual_output !== null && (
            <p><span className="text-gray-500">отримано:</span> <span className="text-white">{result.actual_output || '(порожньо)'}</span></p>
          )}
          {!result.passed && result.expected_output !== null && (
            <p><span className="text-gray-500">очікувалось:</span> <span className="text-green-400">{result.expected_output}</span></p>
          )}
          {result.error && (
            <p className="text-red-400 break-words">{result.error}</p>
          )}
        </div>
      )}
    </div>
  )
}

import { useState } from 'react'
import clsx from 'clsx'
import { useQuizStore } from '../../store/gameStore'
import { quizApi } from '../../services/api'
import { HpBar, Button, Card } from '../ui'

const OPTIONS = ['a', 'b', 'c', 'd'] as const
const OPTION_LABEL: Record<string, string> = { a: 'A', b: 'B', c: 'C', d: 'D' }

interface QuizBattleProps {
  onFinish: (result: { score: number; noDeathRun: boolean; perfectScore: boolean; newAchievements: string[] }) => void
}

export function QuizBattle({ onFinish }: QuizBattleProps) {
  const store = useQuizStore()
  const [selected, setSelected] = useState<string | null>(null)
  const [isAnswering, setIsAnswering] = useState(false)

  const { currentQuestion, sessionId, heroHp, maxHp, questionNumber, totalQuestions, showResult, lastAnswer } = store

  const getOptionText = (opt: string) => {
    if (!currentQuestion) return ''
    return currentQuestion[`option_${opt}` as keyof typeof currentQuestion] as string
  }

  const handleAnswer = async (option: string) => {
    if (!currentQuestion || !sessionId || isAnswering || showResult) return
    setSelected(option)
    setIsAnswering(true)

    try {
      const answer = await quizApi.answer(sessionId, currentQuestion.id, option)
      store.setAnswer(answer)

      if (answer.is_quiz_done) {
        setTimeout(() => {
          onFinish({
            score: answer.final_score ?? store.correctAnswers,
            noDeathRun: answer.no_death_run ?? false,
            perfectScore: answer.perfect_score ?? false,
            newAchievements: answer.new_achievements ?? [],
          })
        }, 2500)
      }
      if (answer.hero_died) {
        // Пауза перед рестартом
        setTimeout(() => store.reset(), 2500)
      }
    } finally {
      setIsAnswering(false)
    }
  }

  const handleNext = () => {
    setSelected(null)
    store.nextQuestion()
  }

  if (!currentQuestion) return null

  return (
    <div className="max-w-2xl mx-auto space-y-5">
      {/* HUD */}
      <div className="flex items-center justify-between gap-4">
        <HpBar current={heroHp} max={maxHp} label="❤️ HP Героя" size="md" />
        <div className="text-gray-400 text-sm whitespace-nowrap">
          {questionNumber} / {totalQuestions}
        </div>
      </div>

      {/* Прогрес крипів */}
      <div className="flex gap-1">
        {Array.from({ length: totalQuestions }).map((_, i) => (
          <div
            key={i}
            className={clsx(
              'h-1.5 flex-1 rounded-full transition-colors',
              i < questionNumber - 1
                ? 'bg-green-500'
                : i === questionNumber - 1
                ? 'bg-yellow-400'
                : 'bg-gray-700'
            )}
          />
        ))}
      </div>

      {/* Питання */}
      <Card className="space-y-4">
        <div className="flex items-start justify-between gap-2">
          <h2 className="text-white text-lg font-medium leading-snug">{currentQuestion.question_text}</h2>
          <span className="text-yellow-400 font-bold text-xl shrink-0">⚔️</span>
        </div>

        {/* Кодовий блок */}
        {currentQuestion.code_snippet && (
          <pre className="bg-gray-950 border border-gray-700 rounded-lg p-4 text-sm text-green-300 font-mono overflow-x-auto whitespace-pre-wrap">
            {currentQuestion.code_snippet}
          </pre>
        )}

        {/* Варіанти відповідей */}
        <div className="grid grid-cols-1 gap-3">
          {OPTIONS.map((opt) => {
            const isSelected = selected === opt
            const isCorrect = showResult && opt === lastAnswer?.correct_option
            const isWrong = showResult && isSelected && opt !== lastAnswer?.correct_option

            return (
              <button
                key={opt}
                onClick={() => handleAnswer(opt)}
                disabled={showResult || isAnswering}
                className={clsx(
                  'w-full text-left px-4 py-3 rounded-xl border-2 transition-all duration-200 text-sm',
                  'disabled:cursor-not-allowed',
                  isCorrect
                    ? 'border-green-500 bg-green-900/50 text-green-300'
                    : isWrong
                    ? 'border-red-500 bg-red-900/50 text-red-300'
                    : isSelected
                    ? 'border-yellow-400 bg-yellow-900/30 text-yellow-300'
                    : 'border-gray-600 bg-gray-700 text-gray-200 hover:border-yellow-500 hover:bg-gray-600'
                )}
              >
                <span className="font-bold mr-3 text-gray-400">{OPTION_LABEL[opt]}.</span>
                {getOptionText(opt)}
                {isCorrect && <span className="float-right">✅</span>}
                {isWrong && <span className="float-right">❌</span>}
              </button>
            )
          })}
        </div>
      </Card>

      {/* Результат після відповіді */}
      {showResult && lastAnswer && !lastAnswer.hero_died && !lastAnswer.is_quiz_done && (
        <Card className={clsx(
          'border-l-4',
          lastAnswer.is_correct ? 'border-l-green-500' : 'border-l-red-500'
        )}>
          <div className="flex items-start justify-between">
            <div>
              <p className={clsx('font-bold mb-1', lastAnswer.is_correct ? 'text-green-400' : 'text-red-400')}>
                {lastAnswer.is_correct ? '⚔️ Крипа вбито! +' + lastAnswer.xp_gained + ' XP' : '💔 Неправильно! Крип атакував!'}
              </p>
              <p className="text-gray-400 text-sm">{lastAnswer.explanation}</p>
            </div>
            <Button size="sm" onClick={handleNext}>
              Далі →
            </Button>
          </div>
        </Card>
      )}

      {/* Герой помер */}
      {showResult && lastAnswer?.hero_died && (
        <Card className="border-l-4 border-l-red-600 text-center">
          <p className="text-red-400 text-xl font-bold mb-2">💀 Герой загинув!</p>
          <p className="text-gray-400">{lastAnswer.explanation}</p>
          <p className="text-gray-500 text-sm mt-2">Повертаємось до початку...</p>
        </Card>
      )}
    </div>
  )
}

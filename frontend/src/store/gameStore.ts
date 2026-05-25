import { create } from 'zustand'
import type { Question, AnswerResponse, BossStartResponse, BossSubmitResponse, TestResult } from '../types'

// ===== QUIZ STORE =====
interface QuizState {
  sessionId: string | null
  locationSlug: string | null
  locationName: string | null
  heroHp: number
  maxHp: number
  questionNumber: number
  totalQuestions: number
  correctAnswers: number

  currentQuestion: Question | null
  lastAnswer: AnswerResponse | null
  showResult: boolean   // показуємо пояснення після відповіді
  isFinished: boolean
  isLoading: boolean

  setSession: (data: {
    sessionId: string; locationSlug: string; locationName: string
    heroHp: number; maxHp: number; question: Question
    questionNumber: number; totalQuestions: number
  }) => void
  setAnswer: (answer: AnswerResponse) => void
  nextQuestion: () => void
  reset: () => void
  setLoading: (v: boolean) => void
}

export const useQuizStore = create<QuizState>()((set) => ({
  sessionId: null,
  locationSlug: null,
  locationName: null,
  heroHp: 5,
  maxHp: 5,
  questionNumber: 1,
  totalQuestions: 10,
  correctAnswers: 0,
  currentQuestion: null,
  lastAnswer: null,
  showResult: false,
  isFinished: false,
  isLoading: false,

  setSession: (data) => set({
    sessionId: data.sessionId,
    locationSlug: data.locationSlug,
    locationName: data.locationName,
    heroHp: data.heroHp,
    maxHp: data.maxHp,
    questionNumber: data.questionNumber,
    totalQuestions: data.totalQuestions,
    currentQuestion: data.question,
    correctAnswers: 0,
    lastAnswer: null,
    showResult: false,
    isFinished: false,
  }),

  setAnswer: (answer) =>
    set((state) => ({
      lastAnswer: answer,
      showResult: true,
      heroHp: answer.hero_hp,
      correctAnswers: answer.is_correct ? state.correctAnswers + 1 : state.correctAnswers,
      isFinished: answer.is_quiz_done || answer.hero_died || false,
    })),

  nextQuestion: () =>
    set((state) => {
      if (!state.lastAnswer?.next_question) return { showResult: false }
      return {
        showResult: false,
        currentQuestion: state.lastAnswer.next_question,
        questionNumber: state.lastAnswer.question_number ?? state.questionNumber + 1,
      }
    }),

  reset: () => set({
    sessionId: null, locationSlug: null, locationName: null,
    heroHp: 5, maxHp: 5, questionNumber: 1, totalQuestions: 10,
    correctAnswers: 0, currentQuestion: null, lastAnswer: null,
    showResult: false, isFinished: false, isLoading: false,
  }),

  setLoading: (v) => set({ isLoading: v }),
}))

// ===== BOSS STORE =====
interface BossState {
  sessionId: string | null
  locationSlug: string | null

  bossData: BossStartResponse['boss'] | null
  challengeData: BossStartResponse['challenge'] | null

  heroHp: number
  maxHp: number
  bossHp: number
  maxBossHp: number

  hintsAvailable: number
  hintsUsed: number
  attemptNumber: number

  testResults: TestResult[]
  lastSubmit: BossSubmitResponse | null
  currentHint: string | null

  isWon: boolean
  isLost: boolean
  isSubmitting: boolean

  setSession: (data: BossStartResponse, maxHp: number) => void
  setSubmitResult: (res: BossSubmitResponse) => void
  setHint: (text: string, hintsUsed: number, heroHp: number, heroDied: boolean) => void
  reset: () => void
  setSubmitting: (v: boolean) => void
}

export const useBossStore = create<BossState>()((set) => ({
  sessionId: null,
  locationSlug: null,
  bossData: null,
  challengeData: null,
  heroHp: 5,
  maxHp: 5,
  bossHp: 100,
  maxBossHp: 100,
  hintsAvailable: 3,
  hintsUsed: 0,
  attemptNumber: 0,
  testResults: [],
  lastSubmit: null,
  currentHint: null,
  isWon: false,
  isLost: false,
  isSubmitting: false,

  setSession: (data, maxHp) => set({
    sessionId: data.session_id,
    bossData: data.boss,
    challengeData: data.challenge,
    heroHp: data.hero_hp,
    maxHp,
    bossHp: data.boss.hp,
    maxBossHp: data.boss.hp,
    hintsAvailable: data.hints_available,
    hintsUsed: data.hints_used,
    attemptNumber: 0,
    testResults: [],
    lastSubmit: null,
    currentHint: null,
    isWon: false,
    isLost: false,
  }),

  setSubmitResult: (res) => set((state) => ({
    lastSubmit: res,
    bossHp: res.boss_hp,
    heroHp: res.hero_hp,
    testResults: res.test_results,
    attemptNumber: state.attemptNumber + 1,
    isWon: res.is_won,
    isLost: res.hero_died || false,
  })),

  setHint: (text, hintsUsed, heroHp, heroDied) => set({
    currentHint: text,
    hintsUsed,
    heroHp,
    isLost: heroDied,
  }),

  reset: () => set({
    sessionId: null, locationSlug: null, bossData: null, challengeData: null,
    heroHp: 5, maxHp: 5, bossHp: 100, maxBossHp: 100,
    hintsAvailable: 3, hintsUsed: 0, attemptNumber: 0,
    testResults: [], lastSubmit: null, currentHint: null,
    isWon: false, isLost: false, isSubmitting: false,
  }),

  setSubmitting: (v) => set({ isSubmitting: v }),
}))

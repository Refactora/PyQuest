// ===== AUTH =====
export interface User {
  id: string
  username: string
  email: string
  avatar_id: number
  level: number
  xp: number
  xp_to_next: number
  total_xp: number
  hp_max: number
  streak_days: number
  created_at?: string
}

export interface AuthResponse {
  user: User
  access_token: string
  token_type: string
}

// ===== LOCATIONS =====
export type LocationStatus = 'locked' | 'available' | 'in_progress' | 'completed'

export interface LocationProgress {
  status: LocationStatus
  quiz_completed: boolean
  boss_defeated: boolean
  best_quiz_score: number
  quiz_attempts: number
  boss_attempts: number
  no_death_run: boolean
  first_try_boss: boolean
  completed_at: string | null
}

export interface Location {
  id: number
  slug: string
  name: string
  description: string
  topic: string
  order_index: number
  boss_name: string
  boss_sprite_id: string
  background_id: string
  enemy_sprite_id: string
  color_theme: string
  progress: LocationProgress
  boss?: BossInfo
}

export interface BossInfo {
  id: number
  title: string
  story_text: string
  task_text: string
  function_signature: string
  starter_code: string
  hints_count: number
  boss_hp: number
  test_cases_visible: VisibleTestCase[]
}

export interface VisibleTestCase {
  input: string
  expected_output: string
  description: string
}

// ===== QUIZ =====
export interface Question {
  id: number
  question_text: string
  code_snippet: string | null
  option_a: string
  option_b: string
  option_c: string
  option_d: string
  difficulty: number
}

export interface QuizStartResponse {
  session_id: string
  location: { id: number; slug: string; name: string }
  hero_hp: number
  question_number: number
  total_questions: number
  question: Question
}

export interface AnswerResponse {
  is_correct: boolean
  correct_option: string
  explanation: string
  xp_gained: number
  hero_hp: number
  hero_died?: boolean
  questions_left?: number
  is_quiz_done: boolean
  restart_message?: string
  creep_killed?: boolean
  next_question?: Question
  question_number?: number
  // Фінальні поля
  final_score?: number
  total_questions?: number
  bonus_xp?: number
  next_step?: string
  no_death_run?: boolean
  perfect_score?: boolean
  new_achievements?: string[]
}

export interface QuizSessionState {
  session_id: string
  hero_hp: number
  question_number: number
  total_questions: number
  correct_answers: number
  question: Question
}

// ===== BOSS FIGHT =====
export interface BossStartResponse {
  session_id: string
  boss: { name: string; hp: number; sprite_id: string }
  challenge: {
    id: number
    title: string
    story_text: string
    task_text: string
    function_signature: string
    starter_code: string
    visible_test_cases: VisibleTestCase[]
  }
  hero_hp: number
  hints_available: number
  hints_used: number
}

export interface TestResult {
  passed: boolean
  actual_output: string | null
  expected_output: string | null
  is_hidden: boolean
  error: string | null
  status: string
  description: string
}

export interface BossSubmitResponse {
  is_won: boolean
  hero_died?: boolean
  boss_hp: number
  hero_hp: number
  test_results: TestResult[]
  passed_count: number
  total_count: number
  boss_damage?: number
  attempt_number?: number
  xp_gained?: number
  first_try?: boolean
  no_hints?: boolean
  new_achievements?: string[]
  message?: string
}

export interface HintResponse {
  hint_text: string
  hp_cost: number
  hero_hp: number
  hero_died: boolean
  hints_used: number
}

// ===== PROFILE =====
export interface ProfileResponse extends User {
  title: string
  stats: {
    locations_completed: number
    total_quiz_attempts: number
    total_boss_attempts: number
  }
  completed_locations: CompletedLocation[]
  achievements: Achievement[]
  streak_bonus: number
}

export interface CompletedLocation {
  location_id: number
  quiz_score: number
  boss_attempts: number
  first_try: boolean
  no_death: boolean
  completed_at: string | null
}

export interface Achievement {
  id: number
  slug: string
  name: string
  description: string
  icon_id: string
  xp_reward: number
}

// ===== LEADERBOARD =====
export interface LeaderboardEntry {
  rank: number
  user_id: string
  username: string
  avatar_id: number
  level: number
  title: string
  total_xp: number
  is_me: boolean
}

export interface LeaderboardResponse {
  leaderboard: LeaderboardEntry[]
  my_rank: number | null
  my_entry: LeaderboardEntry | null
  total_players: number
}

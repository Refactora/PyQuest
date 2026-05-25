import clsx from 'clsx'

// ===== HP Bar =====
interface HpBarProps {
  current: number
  max: number
  label?: string
  size?: 'sm' | 'md' | 'lg'
  color?: 'green' | 'red' | 'blue'
}

export function HpBar({ current, max, label, size = 'md', color = 'green' }: HpBarProps) {
  const pct = Math.max(0, Math.min(100, (current / max) * 100))
  const barColor = pct > 50 ? 'bg-green-500' : pct > 25 ? 'bg-yellow-500' : 'bg-red-500'

  const heights: Record<string, string> = { sm: 'h-2', md: 'h-3', lg: 'h-4' }

  return (
    <div className="w-full">
      {label && (
        <div className="flex justify-between text-sm mb-1 text-gray-300">
          <span>{label}</span>
          <span className="font-bold">{current}/{max}</span>
        </div>
      )}
      <div className={clsx('w-full bg-gray-700 rounded-full overflow-hidden', heights[size])}>
        <div
          className={clsx('h-full rounded-full transition-all duration-500', barColor)}
          style={{ width: `${pct}%` }}
        />
      </div>
      {/* HP серця */}
      {label?.toLowerCase().includes('hp') && (
        <div className="flex gap-1 mt-1">
          {Array.from({ length: max }).map((_, i) => (
            <span key={i} className={clsx('text-lg', i < current ? 'text-red-500' : 'text-gray-600')}>
              ♥
            </span>
          ))}
        </div>
      )}
    </div>
  )
}

// ===== XP Bar =====
interface XpBarProps {
  current: number
  total: number
  level: number
}

export function XpBar({ current, total, level }: XpBarProps) {
  const pct = Math.max(0, Math.min(100, (current / total) * 100))
  return (
    <div className="w-full">
      <div className="flex justify-between text-xs text-gray-400 mb-1">
        <span>Рівень {level}</span>
        <span>{current} / {total} XP</span>
      </div>
      <div className="h-2 w-full bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-yellow-400 rounded-full transition-all duration-700"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

// ===== Boss HP Bar =====
interface BossHpBarProps {
  current: number
  max: number
  bossName: string
}

export function BossHpBar({ current, max, bossName }: BossHpBarProps) {
  const pct = Math.max(0, Math.min(100, (current / max) * 100))
  const color = pct > 60 ? 'bg-red-600' : pct > 30 ? 'bg-orange-500' : 'bg-yellow-400'
  return (
    <div className="w-full">
      <div className="flex justify-between text-sm mb-1">
        <span className="text-red-400 font-bold">👹 {bossName}</span>
        <span className="text-gray-300">{current}/{max} HP</span>
      </div>
      <div className="h-4 w-full bg-gray-700 rounded-full overflow-hidden border border-red-900">
        <div
          className={clsx('h-full rounded-full transition-all duration-700', color)}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

// ===== Badge =====
interface BadgeProps {
  children: React.ReactNode
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info'
}

export function Badge({ children, variant = 'default' }: BadgeProps) {
  const variants: Record<string, string> = {
    default: 'bg-gray-700 text-gray-300',
    success: 'bg-green-900 text-green-300',
    warning: 'bg-yellow-900 text-yellow-300',
    danger: 'bg-red-900 text-red-300',
    info: 'bg-blue-900 text-blue-300',
  }
  return (
    <span className={clsx('px-2 py-0.5 rounded text-xs font-medium', variants[variant])}>
      {children}
    </span>
  )
}

// ===== Button =====
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  loading?: boolean
}

export function Button({ children, variant = 'primary', size = 'md', loading, className, disabled, ...props }: ButtonProps) {
  const variants: Record<string, string> = {
    primary: 'bg-yellow-500 hover:bg-yellow-400 text-black font-bold',
    secondary: 'bg-gray-700 hover:bg-gray-600 text-white',
    danger: 'bg-red-700 hover:bg-red-600 text-white',
    ghost: 'bg-transparent hover:bg-gray-800 text-gray-300 border border-gray-600',
  }
  const sizes: Record<string, string> = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-base',
    lg: 'px-7 py-3 text-lg',
  }
  return (
    <button
      className={clsx(
        'rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed',
        variants[variant], sizes[size], className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? <span className="animate-spin inline-block mr-2">⚙️</span> : null}
      {children}
    </button>
  )
}

// ===== Card =====
export function Card({ children, className }: { children: React.ReactNode; className?: string }) {
  return (
    <div className={clsx('bg-gray-800 border border-gray-700 rounded-xl p-5', className)}>
      {children}
    </div>
  )
}

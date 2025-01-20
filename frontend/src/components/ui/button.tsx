import { FC, ReactNode } from 'react'

interface ButtonProps {
  className?: string
  children: ReactNode
  onClick: () => void
  disabled?: boolean
}

const Button: FC<ButtonProps> = ({ children, onClick, disabled }) => {
  return (
    <button
      className="rounded-md bg-blue-500 px-5 py-2 text-sm text-green-100 shadow-lg hover:bg-blue-900"
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  )
}

export { Button }

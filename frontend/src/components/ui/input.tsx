import { FC } from 'react'

interface InputInterface {
  type: string
  placeholder: string
  value: string
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void
  className: string
}

const Input: FC<InputInterface> = ({
  type,
  placeholder,
  value,
  onChange,
  className
}) => {
  return (
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={className}
    />
  )
}

export { Input }

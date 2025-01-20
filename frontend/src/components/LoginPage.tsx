import BACKEND_URL from 'constants'
import { FormEvent, useState } from 'react'
import { useNavigate } from 'react-router'

const LoginPage = () => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const navigate = useNavigate()
  const validateForm = () => {
    if (!username || !password) {
      setError('Username is required')
      return false
    }
    setError('')
    return true
  }

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault()
    if (!validateForm()) return
    setLoading(true)

    const body = new URLSearchParams({
      grant_type: 'password',
      username: username,
      password: password,
      scope: '',
      client_id: 'string',
      client_secret: 'string'
    })
    try {
      const response = await fetch(`${BACKEND_URL}/api/token`, {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: body.toString()
      })
      setLoading(false)

      if (response.ok) {
        const data = await response.json()
        localStorage.setItem('token', data.access_token)
        navigate('/app')
      } else {
        const errorData = await response.json()
        console.log({ errorData })
        setError(errorData?.detail || 'Login failed.')
      }
    } catch (error) {
      setLoading(false)
      console.log({ error })
      if (error instanceof Error) {
        setError(error.message)
      } else {
        setError('An error occurred. Please try again.')
      }
    }
  }

  return (
    <div className="flex justify-center align-middle">
      <div className="p-4">
        <form onSubmit={handleSubmit}>
          <h1 className="mb-4 text-2xl font-semibold">Login page</h1>
          {error && <p className="mb-2 text-red-700">{error}</p>}
          <div className="mb-4 flex flex-col">
            <label htmlFor="username">Username</label>
            <input
              placeholder="Enter sername"
              className="px-2 py-1"
              id="username"
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div className="mb-4 flex flex-col">
            <label htmlFor="password">Password</label>
            <input
              placeholder="Enter password"
              className="px-2 py-1"
              id="password"
              type="password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div className="flex flex-row items-center justify-between">
            <button
              className="rounded-md bg-blue-400 px-5 py-2 text-sm text-green-100 shadow-lg hover:bg-blue-900"
              disabled={loading || !username || !password}
              type="submit"
            >
              Login
            </button>
            <a className="text-blue-500 underline" href="/register">
              Create an account
            </a>
          </div>
        </form>
      </div>
    </div>
  )
}

export default LoginPage

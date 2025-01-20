import { FC, useEffect, useState } from 'react'
import { useNavigate } from 'react-router'
import BACKEND_URL from 'constants'
import { Input } from './ui/input'
import { Button } from './ui/button'

export interface Participant {
  id: number
  name: string
  blacklisted: number[]
}

export interface Assignment {
  giver_id: number
  receiver_id: number
}

export interface Draw {
  id: number
  date: string
  assignments: Assignment[]
}

const SantaPage: FC = () => {
  const navigate = useNavigate()
  const [participants, setParticipants] = useState<Participant[]>([])
  const [draws, setDraws] = useState<Draw[]>([])
  const [newParticipant, setNewParticipant] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchParticipants = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BACKEND_URL}/api/participants`)
      const data = await response.json()
      setParticipants(data)
      setLoading(false)
    } catch (err: unknown) {
      setLoading(false)
      console.log(err)
      setError('Failed to fetch participants')
    }
  }

  const fetchDraws = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BACKEND_URL}/api/draws`)
      const data = await response.json()
      setDraws(data)
      setLoading(false)
    } catch (err: unknown) {
      setLoading(false)
      console.log(err)
      setError('Failed to fetch draws')
    }
  }

  const addParticipant = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BACKEND_URL}/api/participants`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newParticipant })
      })
      if (!response.ok) throw new Error('Failed to add participant')
      setNewParticipant('')
      void fetchParticipants()
      setLoading(false)
    } catch (err: unknown) {
      setLoading(false)
      console.log(err)
      setError('Failed to add participant')
    }
  }

  const performDraw = async () => {
    setLoading(true)
    try {
      const response = await fetch(`${BACKEND_URL}/api/draws`, {
        method: 'POST'
      })
      if (!response.ok) throw new Error('Failed to perform draw')
      void fetchDraws()
      setLoading(false)
    } catch (err: unknown) {
      console.log(err)
      setError('Failed to perform draw')
      setLoading(false)
    }
  }

  useEffect(() => {
    const verifyToken = async () => {
      setLoading(true)
      const token = localStorage.getItem('token')
      console.log({ token })
      try {
        const response = await fetch(`${BACKEND_URL}/api/verify-token/${token}`)
        if (!response.ok) {
          throw new Error('Token validation failed')
        } else {
          void fetchParticipants()
          void fetchDraws()
        }
        setLoading(false)
      } catch (error) {
        // localStorage.removeItem('token')
        navigate('/login')
        console.log({ error })
      }
      setLoading(false)
    }

    void verifyToken()
  }, [navigate])

  return (
    <div className="container m-auto">
      {loading && <div>Loading...</div>}

      {error && (
        <div className="mb-2 border-red-200 bg-red-100 px-2 py-4 text-red-900">
          {error}
        </div>
      )}

      {!loading && (
        <div>
          <div className="container mb-4 bg-slate-50 p-2">
            <h2 className="text-2xl font-semibold">Add Participant</h2>
            <div>
              <div className="">
                <Input
                  type="text"
                  value={newParticipant}
                  onChange={(e) => setNewParticipant(e.target.value)}
                  placeholder="Participant name"
                  className="mr-2 px-2 py-1"
                />
                <Button
                  disabled={loading || newParticipant.length === 0}
                  onClick={addParticipant}
                >
                  Add
                </Button>
              </div>
            </div>
          </div>

          <div className="container mb-4 bg-slate-50 p-2">
            <h2 className="text-2xl font-semibold">Participants</h2>
            <div>
              <div className="">
                {participants.map((participant) => (
                  <div key={participant.id} className="">
                    {participant.name}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="container mb-4 bg-slate-50 p-2">
            <h2 className="text-2xl font-semibold">Draw History</h2>
            <Button disabled={loading} onClick={performDraw}>
              Perform New Draw
            </Button>

            <div className="mt-4">
              {draws.map((draw) => (
                <div key={draw.id} className="mb-4">
                  <h3 className="font-semibold">
                    Draw {draw.id} - {new Date(draw.date).toLocaleDateString()}
                  </h3>
                  <div className="">
                    {draw.assignments.map((assignment, index) => {
                      const giver = participants.find(
                        (p) => p.id === assignment.giver_id
                      )
                      const receiver = participants.find(
                        (p) => p.id === assignment.receiver_id
                      )
                      return (
                        <div key={index}>
                          {giver?.name} → {receiver?.name}
                        </div>
                      )
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default SantaPage

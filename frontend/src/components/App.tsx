import { Route, Routes } from 'react-router'
import WelcomePage from './WelcomePage'
import SantaPage from './SantaPage'

function App() {
  return (
    <>
      <header className="mb-4 px-2">
        <h1 className="text-center text-2xl font-semibold">Secret Santa 🎅</h1>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<WelcomePage />} />
          <Route path="/app" element={<SantaPage />} />
        </Routes>
      </main>
    </>
  )
}

export default App
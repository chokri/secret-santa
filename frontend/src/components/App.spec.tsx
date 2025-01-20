import { render, screen } from '@testing-library/react'

import App from './App'
import { MemoryRouter } from 'react-router'

describe('<App />', () => {
  it('should render the App', () => {
    const { container } = render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    )

    expect(screen.getByText(/Secret Santa./i)).toBeInTheDocument()

    expect(container.firstChild).toBeInTheDocument()
  })
})

# Documentation

## Tech stack

- Backend Framework: FastAPI, Python
- Database ORM: SQLAlchemy, SQLite
- Data Validation: Pydantic
- Frontend Interface: React + TypeScript + Vite

## Oauth2 authentication

The `OAuth2Password` class from FastAPI’s security module was used for its integration with access tokens. These tokens enable role-based authorization, ensuring users only access endpoints permitted for their assigned roles.

Token expiration is configured via the `ACCESS_TOKEN_EXPIRE_MINUTES` environment variable, which defines the validity duration (in minutes) of generated access tokens.

## Database Models

```python
class Participant(Base):
    __tablename__ = "participants"
    id = Column(Integer, primary_key=True)
    blacklisted = relationship("Participant")  # Self-referential relationship for blacklist

class Draw(Base):
    __tablename__ = "draws"
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    assignments = relationship("Assignment", back_populates="draw")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True)
    draw_id = Column(Integer, ForeignKey("draws.id"))
    giver_id = Column(Integer, ForeignKey("participants.id"))
    receiver_id = Column(Integer, ForeignKey("participants.id"))
    draw = relationship("Draw", back_populates="assignments")
```

## Frontend

The React Application is based on this boilerplate `https://github.com/joaopaulomoraes/reactjs-vite-tailwindcss-boilerplate`

This Boilerplate is build with `Vite`, `React 18`, `TypeScript`, `Vitest`, `Testing Library`, `TailwindCSS 3`, `Eslint` and `Prettier`.

## Dockerisation

Both backend and frontend are dockerized so we can ship them anyway.

## database

The Backend uses SQLite for development purpose.

## Bugs

I had a big issue building the frontend in Docker on my MacBook Pro M1. When I used node:20-alpine, it shows me the following issue:

```bash
[cause]: Error: Cannot find module '@rollup/rollup-linux-arm64-gnu'
react-frontend   |   Require stack:
react-frontend   |   - /app/node_modules/.pnpm/rollup@4.31.0/node_modules/rollup/dist/native.js
```

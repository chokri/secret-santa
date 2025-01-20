
# Documentations


## Tech stack

- Backend Framework: FastAPI
- Database ORM: SQLAlchemy
- Data Validation: Pydantic
- Frontend Interface: React + TypeScript

## Database Models (SQLAlchemy)
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



## Frontend React App

The React Application is based on this boilerplate `https://github.com/joaopaulomoraes/reactjs-vite-tailwindcss-boilerplate`

This Boilerplate is build with `Vite`, `React 18`, `TypeScript`, `Vitest`, `Testing Library`, `TailwindCSS 3`, `Eslint` and `Prettier`.

## Dockerisation

Both backend and frontend are dockerized so we can ship them anyway.
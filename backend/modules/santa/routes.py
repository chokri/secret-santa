from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from modules.santa.controller import SantaController
from modules.santa.schemas import ParticipantCreate, ParticipantResponse, DrawResponse

router = APIRouter()

# Participant routes
@router.post("/participants/", response_model=ParticipantResponse, tags=["Santa API"])
def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    return SantaController.create_participant(participant, db)

@router.get("/participants/", response_model=List[ParticipantResponse], tags=["Santa API"])
def get_participants(db: Session = Depends(get_db)):
    return SantaController.get_participants(db)

# Draw routes
@router.post("/draws/", tags=["Santa API"])
def create_draw(db: Session = Depends(get_db)):
    return SantaController.create_draw(db)

@router.get("/draws/", tags=["Santa API"])
def get_draws(db: Session = Depends(get_db)):
    return SantaController.get_draws(db)

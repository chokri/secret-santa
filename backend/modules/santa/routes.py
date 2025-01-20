from datetime import datetime
from random import choice, random
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from modules.santa.models import Assignment, Draw, Participant
from modules.santa.schemas import (DrawResponse, ParticipantCreate, ParticipantResponse)

router = APIRouter()

@router.post("/participants/", response_model=ParticipantResponse, tags=["Santa API"])
def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    db_participant = Participant(name=participant.name)
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


@router.get("/participants/", response_model=List[ParticipantResponse], tags=["Santa API"])
def get_participants(db: Session = Depends(get_db)):
    return db.query(Participant).all()


@router.post("/draws/", tags=["Santa API"])
def create_draw(db: Session = Depends(get_db)):
    participants = db.query(Participant).all()

    if len(participants) < 2:
        raise HTTPException(status_code=400, detail="Must be over three participants")

    draw = Draw(date=datetime.now())
    db.add(draw)
    db.flush()

    givers = participants.copy()
    receivers = participants.copy()
    assignments = []

    for giver in givers:
        valid_receivers = [
            r for r in receivers
            if r.id != giver.id and r.id not in [b.id for b in giver.blacklisted]
        ]

        if not valid_receivers:
            db.rollback()
            raise HTTPException(
                status_code=400,
                detail="Not a valid configuration"
            )

        receiver = choice(valid_receivers)
        assignment = Assignment(
            draw_id=draw.id,
            giver_id=giver.id,
            receiver_id=receiver.id
        )
        assignments.append(assignment)
        receivers.remove(receiver)

    db.bulk_save_objects(assignments)
    db.commit()
    db.refresh(draw)

    return DrawResponse(
        id=draw.id,
        date=draw.date.isoformat(),
        assignments=draw.assignments
    )

@router.get("/draws/", tags=["Santa API"])
def get_draws(db: Session = Depends(get_db)):
    draws = db.query(Draw).order_by(Draw.date.desc()).limit(5).all()
    print([
        DrawResponse(
            id=draw.id,
            date=draw.date.isoformat(),
            assignments=draw.assignments
        )
        for draw in draws
    ])
    return [
        DrawResponse(
            id=draw.id,
            date=draw.date.isoformat(),
            assignments=draw.assignments
        )
        for draw in draws
    ]


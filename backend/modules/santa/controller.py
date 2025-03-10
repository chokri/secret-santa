from datetime import datetime
from random import choice
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Type

from modules.santa.models import Participant, Draw, Assignment
from modules.santa.schemas import ParticipantCreate, ParticipantResponse, DrawResponse

class SantaController:

    @staticmethod
    def create_participant(participant: ParticipantCreate, db: Session) -> ParticipantResponse:
        db_participant = Participant(name=participant.name)
        db.add(db_participant)
        db.commit()
        db.refresh(db_participant)
        return db_participant

    @staticmethod
    def get_participants(db: Session) -> list[Type[Participant]]:
        return db.query(Participant).all()

    @staticmethod
    def create_draw(db: Session):
        participants = db.query(Participant).all()

        if len(participants) < 3:
            raise HTTPException(status_code=400, detail="Must be at least three participants")

        draw = Draw(date=datetime.now())
        db.add(draw)
        db.flush()

        givers = participants[:]
        receivers = participants[:]
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

    @staticmethod
    def get_draws(db: Session):
        draws = db.query(Draw).order_by(Draw.date.desc()).limit(5).all()
        return [
            DrawResponse(
                id=draw.id,
                date=draw.date.isoformat(),
                assignments=draw.assignments
            )
            for draw in draws
        ]

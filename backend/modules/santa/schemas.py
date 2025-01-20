from datetime import datetime
from typing import List

from pydantic import BaseModel


class ParticipantBase(BaseModel):
    name: str


class ParticipantCreate(ParticipantBase):
    pass


class ParticipantResponse(ParticipantBase):
    id: int
    blacklisted: List[int] = None

    class Config:
        orm_mode = True


class AssignmentResponse(BaseModel):
    id: int
    draw_id: int
    giver_id: int
    receiver_id: int

    class Config:
        from_attributes = True

class DrawResponse(BaseModel):
    id: int
    date: str
    assignments: List[AssignmentResponse]

    class Config:
        from_attributes = True
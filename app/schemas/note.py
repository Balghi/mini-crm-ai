from pydantic import BaseModel
from datetime import datetime
from app.models.note import NoteStatus

class NoteBase(BaseModel):
    raw_text: str

class NoteCreate(NoteBase):
    pass

class NoteRead(NoteBase):
    id: int
    summary: str | None
    status: NoteStatus
    created_at: datetime
    owner_id: int

    class Config:
        from_attributes = True
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.models.user import User, UserRole
from app.models.note import Note, NoteStatus 
from app.worker import summarize_note_task 
from app.schemas.note import NoteCreate, NoteRead

router = APIRouter()

@router.post("/", response_model=NoteRead, status_code=status.HTTP_202_ACCEPTED)
def create_note(
    *,
    db: Session = Depends(deps.get_db),
    note_in: NoteCreate,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Create a new note. This will queue the summarization job.
    """
    # The status now defaults to QUEUED in the model, so we don't need to set it here.
    db_note = Note(**note_in.dict(), owner_id=current_user.id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)

    # 2. DISPATCH THE BACKGROUND TASK
    summarize_note_task.delay(db_note.id)

    return db_note

@router.get("/{note_id}", response_model=NoteRead)
def get_note(
    *,
    db: Session = Depends(deps.get_db),
    note_id: int,
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get a specific note by ID.
    - Agents can only see their own notes.
    - Admins can see any note.
    """
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if current_user.role != UserRole.ADMIN and note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    return note

@router.get("/", response_model=List[NoteRead])
def get_notes(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    """
    Get all notes.
    - Agents can only see their own notes.
    - Admins can see all notes.
    """
    if current_user.role == UserRole.ADMIN:
        notes = db.query(Note).all()
    else:
        notes = db.query(Note).filter(Note.owner_id == current_user.id).all()

    return notes
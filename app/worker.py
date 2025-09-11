import time
from celery import Celery
from transformers import pipeline

from app.db.session import SessionLocal
from app.models.note import Note, NoteStatus
from app.core.config import CELERY_BROKER_URL

# Initialize Celery
celery_app = Celery(__name__, broker=CELERY_BROKER_URL)

# Lazy-load the summarizer model
summarizer = None

def get_summarizer():
    global summarizer
    if summarizer is None:
        # This will download the model on the first run.
        # Using a smaller model for quicker setup.
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-6-6")
    return summarizer

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def summarize_note_task(self, note_id: int):
    """
    Background task to summarize a note's text using an AI model.
    """
    db = SessionLocal()
    try:
        note = db.query(Note).filter(Note.id == note_id).first()
        if not note:
            print(f"Note with ID {note_id} not found.")
            return

        # 1. Update status to PROCESSING
        note.status = NoteStatus.PROCESSING
        db.commit()

        # 2. Perform summarization
        model = get_summarizer()
        summary_list = model(note.raw_text, max_length=150, min_length=30, do_sample=False)
        summary_text = summary_list[0]['summary_text']

        # 3. Update note with summary and set status to DONE
        note.summary = summary_text
        note.status = NoteStatus.DONE
        db.commit()
        print(f"Successfully summarized note {note_id}")

    except Exception as e:
        # 4. On failure, set status to FAILED
        print(f"Task for note {note_id} failed: {e}")
        db.rollback()
        note = db.query(Note).filter(Note.id == note_id).first()
        if note:
            note.status = NoteStatus.FAILED
            db.commit()
        raise e  # Re-raise the exception to trigger Celery's retry mechanism
    finally:
        db.close()
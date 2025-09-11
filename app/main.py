from fastapi import FastAPI
from app.api.routes import auth, notes

app = FastAPI(title="AI Summarizer API")

# Include routers
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(notes.router, prefix="/api/v1/notes", tags=["notes"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Summarizer API"}
from fastapi import FastAPI

# Database
from app.core.database import Base, engine

# Models (important: ensures table creation)
from app.models.user import User
from app.models.document import Document

# Routers
from app.api.auth import router as auth_router
from app.api.upload import router as upload_router
from app.api.query import router as query_router



app = FastAPI(title="Enterprise Document Intelligence System")

app.include_router(query_router)
@app.on_event("startup")
def startup():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

# Register API routes
app.include_router(auth_router)
app.include_router(upload_router)

@app.get("/")
def health_check():
    return {"status": "running"}

print("APplication running")

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000
    )


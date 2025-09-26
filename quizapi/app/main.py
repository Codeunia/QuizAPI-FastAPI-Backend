from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .db.connection import close_mongo_connection, connect_to_mongo, db_manager
from .db.init_db import initialize_database
from .routes import quizzes, questions, attempts, admin, auth, users, change_password
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    db = db_manager.db
    await initialize_database(db)
    yield
    await close_mongo_connection()

app = FastAPI(
    title="QuizAPI",
    description="A backend application built using FastAPI for managing quizzes, questions, and user attempts.",
    version="1.0.0",
    lifespan=lifespan,
)

frontend_url = os.environ.get("FRONTEND_URL", "http://localhost:3000")

origins = [
    "http://localhost:3000",
    frontend_url,

]

print(f"Allowed CORS origins: {origins}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=86400,
)


app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(change_password.router, prefix="/api", tags=["Authentication"])

app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(quizzes.router, prefix="/api", tags=["Quizzes"])
app.include_router(questions.router, prefix="/api", tags=["Questions"])
app.include_router(attempts.router, prefix="/api", tags=["Attempts"])
app.include_router(admin.router, prefix="/api", tags=["Admin Panel"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the QuizAPI!"}

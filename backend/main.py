from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import Base, engine
from starlette.middleware.sessions import SessionMiddleware
from Controller import TasksController, CalendarController, AuthController, AgendaController
from dotenv import load_dotenv
from backend.Model import Calendar, Tasks
import uvicorn
import os

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Sistema de Organização de Tarefas", lifespan=lifespan)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "fallback-secret-key"),
    session_cookie="session_cookie"
)

app.include_router(TasksController.router, prefix="/event")
app.include_router(CalendarController.router, prefix="/calendar")
app.include_router(AuthController.router, prefix="/auth")
app.include_router(AgendaController.router, prefix="/read")

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=[],
    allow_headers=[],
)"""

@app.get("/")
def root():
    return {"mensagem": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000 , reload=True)
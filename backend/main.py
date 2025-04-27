from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.database import Base, engine
from Controller import TasksController, CalendarController
from backend.Model import Calendar, Tasks

import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(title="Sistema de Organização de Tarefas", lifespan=lifespan)

app.add_route("/event", TasksController.router)
app.add_route("/calendar", CalendarController.router)

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
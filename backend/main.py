from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from Controller.home import router as home_router
from Controller.tasks import router as tasks_router

app = FastAPI(title="Sistema de Organização de Tarefas")

"""app.add_middleware(
    CORSMiddleware,
    allow_origins=[],
    allow_credentials=True,
    allow_methods=[],
    allow_headers=[],
)"""

# Include the home router
app.include_router(home_router, prefix="/api")
app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
async def root():
    return {"mensagem": "Hello World"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
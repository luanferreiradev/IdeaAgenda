from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"mensagem": "Hello World"}
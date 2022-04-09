from fastapi import FastAPI, Depends

from app.dependencies import get_token_header
from app.routers import dtp


app = FastAPI()

app.include_router(dtp.router)


@app.get("/")
async def root():
    return {"message": "Привет, перейди в документацию чтобы посмотреть все возможности апи! Документация: http://127.0.0.1:8000/docs"}
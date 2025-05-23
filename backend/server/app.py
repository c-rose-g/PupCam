from fastapi import FastAPI
from server.database import init_db
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  await init_db()
  yield

app = FastAPI(lifespan=lifespan)

@app.get("/", tags=["Root"])
async def root() -> dict:
  return {"message:":"Hello World"}

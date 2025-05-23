from fastapi import FastAPI
from server.database import init_db
from contextlib import asynccontextmanager
from server.routes import event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
  await init_db()
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(event_router, prefix="/events", tags=["Events"])

@app.get("/", tags=["Root"])
async def root() -> dict:
  return {"message:":"Hello World"}

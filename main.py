import uvicorn
from fastapi import FastAPI
from app.routers import auth, resources
from contextlib import asynccontextmanager
from app.db import connect_to_mongo, close_mongo_connection, db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()

app = FastAPI(
    title="Intelligent Resource Monitoring & Anomaly Detection API",
    description="A backend system for ingesting resource metrics, evaluating alerts, and detecting anomalies.",
    version="0.1.0",
    lifespan=lifespan
)

@app.get("/", tags=["Health Check"])
async def read_root():
    return {"message": "Welcome to the Intelligent Resource Monitoring API!"}

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication & User Management"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resource Management"])


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
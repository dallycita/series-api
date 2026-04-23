from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import series, ratings, upload
import os

app = FastAPI(
    title="Series Tracker API",
    description="API REST para gestionar tu lista de series",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(series.router)
app.include_router(ratings.router)
app.include_router(upload.router)

@app.get("/")
def root():
    return {"message": "Series Tracker API", "docs": "/docs"}
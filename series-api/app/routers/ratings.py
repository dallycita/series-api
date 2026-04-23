from fastapi import APIRouter, HTTPException
from app.schemas import RatingCreate
from app import crud

router = APIRouter(prefix="/series", tags=["ratings"])

@router.post("/{series_id}/rating", status_code=201)
def add_rating(series_id: int, body: RatingCreate):
    if not crud.get_series_by_id(series_id):
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return crud.create_rating(series_id, body.score, body.review)

@router.get("/{series_id}/rating")
def get_ratings(series_id: int):
    if not crud.get_series_by_id(series_id):
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return crud.get_ratings(series_id)
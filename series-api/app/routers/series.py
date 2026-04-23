from fastapi import APIRouter, HTTPException, Query
from app.schemas import SeriesCreate, SeriesUpdate
from app import crud

router = APIRouter(prefix="/series", tags=["series"])

@router.get("")
def list_series(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    q: str = Query(""),
    sort: str = Query("created_at"),
    order: str = Query("desc")
):
    return crud.get_all_series(page, limit, q, sort, order)

@router.get("/{series_id}")
def get_series(series_id: int):
    row = crud.get_series_by_id(series_id)
    if not row:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    return row

@router.post("", status_code=201)
def create_series(body: SeriesCreate):
    return crud.create_series(body.model_dump())

@router.put("/{series_id}")
def update_series(series_id: int, body: SeriesUpdate):
    if not crud.get_series_by_id(series_id):
        raise HTTPException(status_code=404, detail="Serie no encontrada")
    row = crud.update_series(series_id, body.model_dump())
    return row

@router.delete("/{series_id}", status_code=204)
def delete_series(series_id: int):
    affected = crud.delete_series(series_id)
    if affected == 0:
        raise HTTPException(status_code=404, detail="Serie no encontrada")
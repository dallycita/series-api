from pydantic import BaseModel, Field
from typing import Optional

class SeriesCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    genre: Optional[str] = None
    status: Optional[str] = "pendiente"
    synopsis: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    image_path: Optional[str] = None

class SeriesUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = None
    status: Optional[str] = None
    synopsis: Optional[str] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)
    image_path: Optional[str] = None

class RatingCreate(BaseModel):
    score: float = Field(..., ge=0, le=10)
    review: Optional[str] = None
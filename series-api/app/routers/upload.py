from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os, uuid
from PIL import Image
import io

router = APIRouter(tags=["upload"])

UPLOAD_DIR = "uploads"
MAX_SIZE_BYTES = 1 * 1024 * 1024  # 1 MB
ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}

@router.post("/upload", status_code=201)
async def upload_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG o WebP")

    contents = await file.read()
    if len(contents) > MAX_SIZE_BYTES:
        raise HTTPException(status_code=400, detail="La imagen no puede superar 1 MB")

    # Validar que sea imagen real con Pillow
    try:
        img = Image.open(io.BytesIO(contents))
        img.load()
    except Exception:
        raise HTTPException(status_code=400, detail="Archivo de imagen inválido")

    ext = file.filename.rsplit(".", 1)[-1].lower()
    filename = f"{uuid.uuid4()}.{ext}"
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    with open(os.path.join(UPLOAD_DIR, filename), "wb") as f:
        f.write(contents)

    return JSONResponse({"image_path": f"/uploads/{filename}"})
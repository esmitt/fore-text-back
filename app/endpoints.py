from fastapi import APIRouter, UploadFile, File, HTTPException
from common.logger import logger

router = APIRouter()

@router.get("/")
async def root():
    """
    Simple health check endpoint.
    Returns my name :) to verify the API is operational.
    """
    return {"Test": "esmitt"}

@router.post("/text-foreground", response_model=dict)
async def composer_text(
        image: UploadFile = File(...)
):
    try:
        # Validate image
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
        return {"info": "ok"}
    except Exception as exc:
        logger.error(f"Error processing request on file \'{image.filename}\' ({image.size} bytes): {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
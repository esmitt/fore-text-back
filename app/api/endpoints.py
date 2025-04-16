from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
from core.text import TextFT
import io

from common.logger import logger
from app.schemas.text import TextParameters
import numpy as n

from core.image_loader_from_buffer import ImageLoaderFromBuffer
from core.interfaces.image_loader import ImageLoaderInterface
from core.interfaces.foreground import ForegroundInterface
from core.interfaces.background import BackgroundInterface
from core.foreground import Foreground
from core.background import Background
from core.composer import Composer
from common.utils import Position, RGBAColor
import cv2

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
        image: UploadFile = File(...),
        text_parameter: TextParameters = Depends()
):
    try:
        # validate image
        if not image.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

        # read the image
        image_data: bytes = await image.read()
        image_loader: ImageLoaderInterface = ImageLoaderFromBuffer()
        if not image_loader.set_source(image_data):
            raise HTTPException(status_code=400, detail="Failed to set image buffer")
        if not image_loader.load():
            raise HTTPException(status_code=400, detail="Failed to load image from buffer")

        # initialize components
        foreground: ForegroundInterface = Foreground()
        background: BackgroundInterface = Background()

        # initialize text
        text_ft = TextFT(text=text_parameter.text,
                         font_size=text_parameter.font_size,
                         position=Position(text_parameter.position_x or 0,
                                           text_parameter.position_y or 0),
                         font_color=RGBAColor(r=text_parameter.font_color_r,
                                              g=text_parameter.font_color_g,
                                              b=text_parameter.font_color_b,
                                              a=text_parameter.font_color_a))

        available_fonts = text_ft.get_available_fonts()
        if text_parameter.font_name:
            if text_parameter.font_name not in available_fonts:
                raise HTTPException(
                    status_code=400,
                    detail=f"Font '{text_parameter.font_name}' not available. Available fonts: {available_fonts}"
                )
            text_ft.font_type = text_parameter.font_name
        else:
            text_ft.font_type = available_fonts[0] if available_fonts else None

        # initialize composer
        composer = Composer(image_loader, foreground, background, text_ft)
        output_image = composer.get_output()
        _, buffer = cv2.imencode('.png', output_image)
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/png")
    except Exception as exc:
        logger.error(f"Error processing request on file \'{image.filename}\' ({image.size} bytes): {exc}")
        raise HTTPException(status_code=500, detail=str(exc))
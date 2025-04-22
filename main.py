from core.composer import Composer
from core.interfaces.image_loader import ImageLoaderInterface
from core.image_loader_from_file import ImageLoaderFromFile
from core.foreground import Foreground, ForegroundInterface
from core.background import Background, BackgroundInterface
from core.text import TextFT
from common.utils import Position, RGBAColor, HorizontalAlignment, VerticalAlignment
from common.logger import logger
from dotenv import load_dotenv
from pathlib import Path

if __name__ == "__main__":
    load_dotenv()
    image_loader: ImageLoaderInterface = ImageLoaderFromFile()
    foreground: ForegroundInterface = Foreground()
    background: BackgroundInterface = Background()
    try:
        text_ft: TextFT = TextFT(
            "example",
            font_size=250,
            h_align=HorizontalAlignment.RIGHT,
            v_align=VerticalAlignment.CENTER,
            font_color=RGBAColor(24, 250, 24, 120)
        )
    except Exception as exc:
        logger.exception(f"{exc}")
        exit(0)

    path_sample_image = Path.cwd() / "images" / "WhatsApp Image 2025-03-27 at 07.37.50.jpeg"

    image_loader.set_source(str(path_sample_image))
    list_fonts = text_ft.get_available_fonts()

    composer: Composer = Composer(image_loader, foreground, background, text_ft)
    text_ft.font_type = list_fonts[0]
    success, position = composer.set_text(text_ft)
    output_image, parameters = composer.get_output()

    if output_image is not None and success:
        logger.info(f"First image success: {success}, position: ({position.x}, {position.y}), parameters: {parameters}")
        Composer.show_image(output_image)
    else:
        logger.critical("Failed to get composed image.")
        if output_image is not None:
            Composer.show_image(output_image)  # Show original image if failed

    # Set new text and adjust position
    text_ft.set_text("Impacting more")
    text_ft.font_color = RGBAColor(200, 20, 20)
    text_ft.font_type = list_fonts[1]
    text_ft.h_align = HorizontalAlignment.LEFT
    text_ft.v_align = VerticalAlignment.UP
    success, position = composer.set_text(text_ft)
    output_image, parameters = composer.get_output()

    if output_image is not None and success:
        logger.info(f"Second image success: {success}, position: ({position.x}, {position.y}), parameters: {parameters}")
        Composer.show_image(output_image)

        # Move text
        new_position = Position(position.x + 50, position.y + 200)
        text_ft.set_position(new_position)
        success, position = composer.set_text(text_ft)
        output_image, new_parameters = composer.get_output()

        if output_image is not None and success:
            logger.info(f"Moved image success: {success}, new position: ({position.x}, {position.y}), parameters: {new_parameters}")
            Composer.show_image(output_image)
        else:
            logger.critical("Failed to compose moved image.")
            if output_image is not None:
                Composer.show_image(output_image)  # Show original image if failed
    else:
        logger.critical("Failed to get composed image.")
        if output_image is not None:
            Composer.show_image(output_image)  # Show original image if failed
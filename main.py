from core.composer import Composer
from core.image_loader import ImageLoaderFromFile, ImageLoaderInterface
from core.foreground import Foreground, ForegroundInterface
from core.background import Background, BackgroundInterface
from core.text import TextTTF
from core.common import Position, RGBAColor
from core.logger import logger
from dotenv import load_dotenv
from pathlib import Path

if __name__ == "__main__":
    load_dotenv()
    image_loader: ImageLoaderInterface = ImageLoaderFromFile()
    foreground: ForegroundInterface = Foreground()
    background: BackgroundInterface = Background()
    try:
        text_ttf: TextTTF = TextTTF("example", position=Position(150, 350), font_size=300)
    except Exception as exc:
        logger.exception(f"{exc}")
        exit(0)

    list_fonts = text_ttf.get_available_fonts()

    path_sample_image = Path.cwd() / "images" / "WhatsApp Image 2025-03-27 at 07.37.50.jpeg"
    image_loader.set_source(str(path_sample_image))

    composer: Composer = Composer(image_loader, foreground, background, text_ttf)
    Composer.show_image(composer.get_output())
    text_ttf.set_text("Boludosáé")
    text_ttf.font_color = RGBAColor(r = 210, g = 98, b = 133, a = 200)
    # change font and color and size
    text_ttf.font_size = text_ttf.font_size * 0.5
    text_ttf.font_type = "asda"
    composer.set_text(text_ttf)
    text_ttf.font_size = text_ttf.font_size * 1.6
    Composer.show_image(composer.get_output())
    text_ttf.set_text("Testing")
    text_ttf.font_color = RGBAColor(r = 110, g = 198, b = 13, a = 20)
    text_ttf.font_type = None
    composer.set_text(text_ttf)
    Composer.show_image(composer.get_output())

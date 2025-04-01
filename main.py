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
    except FileNotFoundError:
        logger.exception("The text is built with errors. Not possible to continue (?)")
        exit(0)
    except ReferenceError:
        logger.exception("There are not font files into the folder of fonts")
        exit(0)

    path_sample_image = Path.cwd() / "images" / "WhatsApp Image 2025-03-27 at 07.37.50.jpeg"
    image_loader.set_source(str(path_sample_image))

    composer: Composer = Composer(image_loader, foreground, background, text_ttf)
    Composer.show_image(composer.get_output())
    text_ttf.text = "Boludosáé"
    text_ttf.set_font_color(RGBAColor(r = 210, g = 98, b = 133, a = 200))
    composer.set_text(text_ttf)
    Composer.show_image(composer.get_output())

import os
from core.composer import Composer
from core.image_loader import ImageLoaderFromFile, ImageLoaderInterface
from core.foreground import Foreground, ForegroundInterface
from core.background import Background, BackgroundInterface
from core.text import TextTTF

if __name__ == "__main__":
    image_loader: ImageLoaderInterface = ImageLoaderFromFile()
    foreground: ForegroundInterface = Foreground()
    background: BackgroundInterface = Background()
    text_ttf: TextTTF = TextTTF("example")

    image_loader.set_source(os.path.join(os.getcwd(), "images", "WhatsApp Image 2025-03-27 at 07.37.50.jpeg"))

    composer: Composer = Composer(image_loader, foreground, background, text_ttf)
    Composer.show_image(composer.get_output())
    text_ttf.text = "Boludosáé"
    composer.set_text(text_ttf)
    Composer.show_image(composer.get_output())

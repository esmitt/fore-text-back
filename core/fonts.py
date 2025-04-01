import os
from pathlib import Path
from core.logger import logger
from typing import Dict, List, Optional

class Fonts:
    def __init__(self):
        self._font_path: Path = Path(os.getenv("FONT_FOLDER", "temp_font"))
        if not Path.is_dir(self._font_path):
            logger.critical(f"The folder for fonts, isn't available: `{self._font_path}`")
            raise FileNotFoundError(f"Font folder '{self._font_path}' does not exist")
        self._fonts: Dict[str, str] = {}
        logger.info(f"{self._load_fonts()} fonts loaded")

    def _load_fonts(self) -> int:
        extension_env: str = os.getenv("FONT_EXTENSION", 'abc')
        extension: str = f"*.{extension_env}"

        self._fonts = {}
        for font_file in self._font_path.glob(extension):
            name: str = font_file.stem
            path: str = font_file.resolve()
            self._fonts[name] = path

        return len(self._fonts)

    def get_fonts(self) -> List[str]:
        return list(self._fonts)

    def get_font(self, font_name: str) -> Optional[str]:
        return self._fonts.get(font_name)

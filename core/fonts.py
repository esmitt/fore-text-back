import os
from pathlib import Path
from common.logger import logger
from core.common import get_list_extensions
from typing import Dict, List, Optional

class Fonts:
    def __init__(self):
        """
        Initializes the Fonts engine, finding font files in the specified folder.
        Reads FONT_FOLDER and FONT_EXTENSION from environment variables.
        FONT_EXTENSION can be a comma-separated list (e.g., "ttf,otf").
        """
        self._font_path: Path = Path(os.getenv("FONT_FOLDER", "temp_font"))
        if not Path.is_dir(self._font_path):
            logger.critical(f"The folder for fonts, isn't available: `{self._font_path}`")
            raise FileNotFoundError(f"Font folder '{self._font_path}' does not exist")
        self._fonts: Dict[str, str] = {}
        fonts_loaded: int = self._load_fonts()
        logger.info(f"{fonts_loaded} font(s) loaded from {self._font_path}")

    def _load_fonts(self) -> int:
        """
        Scans the font directory for specified font extensions and populates the
        internal font dictionary.

        Reads FONT_EXTENSION environment variable for a comma-separated list of
        extensions (e.g., "ttf,otf"). The order determines preference if
        duplicate stems exist (first extension listed is preferred).
        Defaults to "ttf" if the variable is not set.

        Returns:
            The number of unique font stems loaded.
        """
        extension_str: str = os.getenv("FONT_EXTENSION", 'ttf')
        extension_list: List[str] = get_list_extensions(extension_str)

        if not extension_list:
            logger.warning("No valid extensions specified in $FONT_EXTENSION")
            return 0

        for extension in extension_list:
            pattern: str = f"*.{extension}"
            try:
                found_fonts: List[Path] = list(self._font_path.glob(pattern))
                for font_file in found_fonts:
                    if font_file.is_file():
                        name: str = font_file.stem
                        if name not in self._fonts:
                            path: str = str(font_file.resolve())
                            self._fonts[name] = path
                            logger.debug(f"Loaded font '{name}' from '{font_file.name}'")
                        else:
                            logger.debug(f"Skipping '{font_file.name}'; font stem '{name}' already loaded from '{Path(self._fonts[name]).name}'.")
            except Exception as exc:
                logger.error(f"Error scanning for {pattern} in {self._font_path}: {exc}", exc_info=True)

        if not self._fonts:
            logger.warning(f"No font files found matching extensions {extension_list} in '{self._font_path}'")

        return len(self._fonts)

    def get_fonts(self) -> List[str]:
        """Returns a list of loaded font names (stems)."""
        return list(self._fonts.keys())

    def get_font(self, font_name: str) -> Optional[str]:
        """
        Gets the absolute path for a given font name (stem).

        Args:
            font_name: The stem name of the font (e.g., "Arial").

        Returns:
            The absolute path string if the font is loaded, otherwise None.
        """
        return self._fonts.get(font_name)

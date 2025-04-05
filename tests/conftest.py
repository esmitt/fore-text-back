import pytest
from pathlib import Path
from typing import Optional
from core.fonts import Fonts
import os
import shutil
from typing import List
from core.common import get_list_extensions

TEST_DIR = Path(__file__).parent
TEST_DATA_DIR = TEST_DIR / "test_data"
FONT_FILE_NAME = "Qalogre.otf"
REAL_FONT_PATH = TEST_DATA_DIR / FONT_FILE_NAME

@pytest.fixture
def setup_real(tmp_path: Path) -> Optional[Fonts]:
    font_folder = tmp_path / "fonts"
    Path.mkdir(font_folder)

    extension = REAL_FONT_PATH.suffix[1:]
    os.environ["FONT_EXTENSION"] = extension

    if not REAL_FONT_PATH.exists():
        pytest.fail(f"Real font file not found at: {REAL_FONT_PATH}")

    # copy the font file into the temp dir
    shutil.copy(REAL_FONT_PATH, font_folder / f"{FONT_FILE_NAME}")

    os.environ["FONT_FOLDER"] = str(font_folder)

    return Fonts()

@pytest.fixture
def setup_fake(tmp_path: Path) -> Optional[Fonts]:
    font_folder = tmp_path / "fonts"
    Path.mkdir(font_folder)

    os.environ["FONT_EXTENSION"] = "otf,ttf"

    # dummy font files for each extension (should be only 2)
    font_extension: str = os.getenv("FONT_EXTENSION")
    extension_list: List[str] = get_list_extensions(font_extension)
    for extension in extension_list:
        Path.touch(font_folder / f"Arial.{extension}")
        Path.touch(font_folder / f"Times New Roman.{extension}")

    os.environ["FONT_FOLDER"] = str(font_folder)

    return Fonts()

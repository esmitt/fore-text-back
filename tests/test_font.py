import pytest
from pathlib import Path
from typing import Optional, List
import os
from core.fonts import Fonts

@pytest.fixture
def setup(tmp_path: Path) -> Optional[Fonts]:
    font_folder = tmp_path / "fonts"
    Path.mkdir(font_folder)

    os.environ["FONT_EXTENSION"] = "ttf"

    # dummy font files
    font_extension: str = os.getenv("FONT_EXTENSION")
    Path.touch(font_folder / f"Arial.{font_extension}")
    Path.touch(font_folder / f"Times New Roman.{font_extension}")

    os.environ["FONT_FOLDER"] = str(font_folder)

    return Fonts()

def test_get_font(setup):
    font_obj = setup

    arial_path = font_obj.get_font("Arial")
    assert arial_path is not None
    assert Path(arial_path).exists()

def test_get_fonts(setup):
    font_obj = setup

    list_fonts = font_obj.get_fonts()
    assert isinstance(list_fonts, list)

def test_load_fonts(setup):
    font_obj = setup

    number_fonts = font_obj._load_fonts()
    assert number_fonts == 2

def test_init():
    os.environ["FONT_FOLDER"] = "a fake folder"
    with pytest.raises(FileNotFoundError):
        Fonts()



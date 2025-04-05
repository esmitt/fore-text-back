import pytest
from pathlib import Path
import os
from core.fonts import Fonts
from tests.conftest import setup_fake

def test_get_font(setup_fake):
    font_obj = setup_fake

    arial_path = font_obj.get_font("Arial")
    assert arial_path is not None
    assert Path(arial_path).exists()

    times_path = font_obj.get_font("Times New Roman")
    assert times_path is not None
    assert Path(times_path).exists()

def test_get_fonts(setup_fake):
    font_obj = setup_fake

    list_fonts = font_obj.get_fonts()
    assert isinstance(list_fonts, list)

def test_load_fonts(setup_fake):
    font_obj = setup_fake

    number_fonts = font_obj._load_fonts()
    assert number_fonts == 2

def test_init():
    os.environ["FONT_FOLDER"] = "a fake folder"
    with pytest.raises(FileNotFoundError):
        Fonts()

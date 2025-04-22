import pytest

from common.utils import RGBAColor, Position
from core.text import TextFT
from PIL.ImageFont import FreeTypeFont
from tests.conftest import setup_real, setup_fake

def test_set_text(setup_real):
    tft_obj = TextFT("Hello")
    assert tft_obj._text == "Hello"
    tft_obj.set_text("world")
    assert tft_obj._text == "world"

def test_get_available_fonts(setup_real):
    tft_obj = TextFT()
    assert isinstance(tft_obj.get_available_fonts(), list)
    assert 1 == len(tft_obj.get_available_fonts())

def test_font_type(setup_real):
    tft_obj = TextFT()
    font_type = tft_obj.font_type
    assert isinstance(font_type, FreeTypeFont)
    assert "Qalogre" == font_type.getname()[0]

def test_font_size(setup_real):
    tft_obj = TextFT(font_size=50)
    assert tft_obj.font_size == 50
    tft_obj.font_size = 100
    assert tft_obj.font_size == 100

def test_font_color(setup_real):
    tft_obj = TextFT(font_color=RGBAColor(50, 50, 50, 128))
    assert tft_obj.font_color == RGBAColor(50, 50, 50, 128)
    tft_obj.font_color = RGBAColor(155, 155, 155, 255)
    assert tft_obj.font_color == RGBAColor(155, 155, 155, 255)

def test_set_position(setup_real):
    tft_obj = TextFT(position=Position(40, 50))
    assert tft_obj._position == Position(40, 50)
    tft_obj._position = Position(20, 25)
    assert tft_obj._position == Position(20, 25)

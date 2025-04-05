import pytest
from core.text import TextTTF
from tests.conftest import setup_real, setup_fake

def test_set_text(setup_real):
    ttf_obj = TextTTF("Hello")
    assert ttf_obj._text == "Hello"
    ttf_obj.set_text("world")
    assert ttf_obj._text == "world"

def test_get_available_fonts(setup_real):
    ttf_obj = TextTTF()
    assert isinstance(ttf_obj.get_available_fonts(), list)
    assert 1 == len(ttf_obj.get_available_fonts())

def test_font_type(setup_real):
    ttf_obj = TextTTF()
    assert "Qalogre" == ttf_obj.font_type.getname()[0]


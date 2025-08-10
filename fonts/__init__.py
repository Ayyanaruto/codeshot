"""
Fonts package for codeshot - beautiful code screenshots
"""

from .config import (
    FONT_FAMILIES,
    DEFAULT_CODE_FONT, 
    DEFAULT_UI_FONT,
    FALLBACK_FONTS,
    get_font_path,
    get_available_fonts,
    get_font_weights,
)

__all__ = [
    "FONT_FAMILIES",
    "DEFAULT_CODE_FONT",
    "DEFAULT_UI_FONT", 
    "FALLBACK_FONTS",
    "get_font_path",
    "get_available_fonts",
    "get_font_weights",
]

"""Core code rendering functionality."""

import io
from typing import Optional
from PIL import Image, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

from config.constants import THEME_MAPPINGS, QUALITY_SCALE


def detect_language(code: str, language: Optional[str] = None) -> str:
    """Auto-detect programming language if not specified."""
    if not language:
        try:
            lexer = guess_lexer(code)
            return lexer.name.lower()
        except:
            return "python"
    return language


def create_code_image(
    code: str, 
    language: str, 
    theme: str, 
    font_size: int, 
    line_numbers: bool = True,
    font_path: Optional[str] = None
) -> Image.Image:
    """Generate syntax highlighted code image."""
    # Get lexer
    try:
        lexer = get_lexer_by_name(language)
    except:
        lexer = get_lexer_by_name("text")
    
    # Map theme to pygments style
    pygments_theme = THEME_MAPPINGS.get(theme, theme)
    
    # Enhanced formatter with ultra-high-quality settings
    formatter_kwargs = {
        "style": pygments_theme,
        "font_size": font_size * QUALITY_SCALE,
        "line_numbers": line_numbers,
        "line_number_chars": 4,
        "line_number_pad": 15 * QUALITY_SCALE,
        "line_number_separator": True,
        "image_format": "PNG",
        "image_pad": 25 * QUALITY_SCALE,
        "image_quality": 100,
    }
    
    # Theme-specific styling
    if theme in ["dracula", "one-dark"]:
        formatter_kwargs.update({
            "line_number_bg": "#1a1b26",
            "line_number_fg": "#565f89", 
            "hl_color": "#414868"
        })
    elif theme == "nord":
        formatter_kwargs.update({
            "line_number_bg": "#2e3440",
            "line_number_fg": "#616e88",
            "hl_color": "#3b4252"
        })
    else:
        formatter_kwargs.update({
            "line_number_bg": "#2d2d2d",
            "line_number_fg": "#8f8f8f", 
            "hl_color": "#3c3c3c"
        })
    
    if font_path:
        formatter_kwargs["font_name"] = font_path
    
    formatter = ImageFormatter(**formatter_kwargs)
    
    # Generate syntax highlighted image at high resolution
    highlighted_img_bytes = highlight(code, lexer, formatter)
    code_img_high_res = Image.open(io.BytesIO(highlighted_img_bytes))
    
    # Scale down with high-quality resampling
    target_width = code_img_high_res.width // QUALITY_SCALE
    target_height = code_img_high_res.height // QUALITY_SCALE
    code_img = code_img_high_res.resize(
        (target_width, target_height), 
        Image.Resampling.LANCZOS
    )
    
    return code_img

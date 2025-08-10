"""Font loading utilities with fallback support."""

from pathlib import Path
from PIL import ImageFont
from typing import Union
import sys


def load_font(font_family: str, size: int, weight: str = "regular") -> Union[ImageFont.FreeTypeFont, ImageFont.ImageFont]:
    """Load a font with fallback to system fonts."""
    fonts_dir = Path(__file__).parent.parent.parent / "fonts"
    sys.path.insert(0, str(fonts_dir.parent))
    
    try:
        from fonts import get_font_path, FALLBACK_FONTS
        
        if font_family != "system":
            font_path = get_font_path(font_family, weight)
            if font_path:
                try:
                    return ImageFont.truetype(str(font_path), size)
                except (OSError, IOError):
                    pass
        
        # Try system fonts
        for fallback_font in FALLBACK_FONTS:
            try:
                return ImageFont.truetype(fallback_font, size)
            except (OSError, IOError):
                continue
                
    except ImportError:
        pass
    
    # Final fallback
    try:
        return ImageFont.truetype("DejaVu Sans Mono", size)
    except (OSError, IOError):
        return ImageFont.load_default()

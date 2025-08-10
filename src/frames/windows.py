"""Windows window frame styling."""

from PIL import ImageDraw
from typing import TYPE_CHECKING, Optional
from src.utils.fonts import load_font

if TYPE_CHECKING:
    from PIL.ImageDraw import ImageDraw as ImageDrawType


def draw_windows_frame(
    draw: "ImageDrawType", 
    frame_width: int, 
    title_bar_height: int, 
    window_title: Optional[str], 
    language: str, 
    font_family: str
) -> None:
    """Draw Windows-style window frame."""
    title_bg = "#2d2d2d"
    draw.rectangle([0, 0, frame_width, title_bar_height], fill=title_bg)
    
    # Window controls (minimize, maximize, close) - Windows 11 style
    button_width = 46
    button_height = title_bar_height
    
    # Close button (red)
    close_x = frame_width - button_width
    draw.rectangle([close_x, 0, frame_width, button_height], fill="#c42b1c")
    draw.text((close_x + 16, 15), "✕", fill="#ffffff", font=load_font(font_family, 12, "regular"))
    
    # Maximize button
    max_x = close_x - button_width
    draw.rectangle([max_x, 0, close_x, button_height], fill="#404040")
    draw.text((max_x + 16, 15), "□", fill="#ffffff", font=load_font(font_family, 12, "regular"))
    
    # Minimize button  
    min_x = max_x - button_width
    draw.rectangle([min_x, 0, max_x, button_height], fill="#404040")
    draw.text((min_x + 16, 15), "—", fill="#ffffff", font=load_font(font_family, 12, "regular"))
    
    # Window title
    title = window_title or f"{language.capitalize()} Code"
    font = load_font(font_family, 12, "regular")
    draw.text((15, 15), title, fill="#ffffff", font=font)

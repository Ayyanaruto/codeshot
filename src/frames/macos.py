"""macOS window frame styling."""

from typing import TYPE_CHECKING, Optional

from PIL import ImageDraw

from src.utils.fonts import load_font

if TYPE_CHECKING:
    from PIL.ImageDraw import ImageDraw as ImageDrawType


def draw_macos_frame(
    draw: "ImageDrawType",
    frame_width: int,
    title_bar_height: int,
    window_title: Optional[str],
    language: str,
    font_family: str,
) -> None:
    """Draw macOS-style window frame."""
    title_bar_color = "#2d2d2d"
    draw.rectangle([0, 0, frame_width, title_bar_height], fill=title_bar_color)
    draw.line(
        [(0, title_bar_height - 1), (frame_width, title_bar_height - 1)], fill="#1a1a1a", width=1
    )

    button_y = title_bar_height // 2
    # Traffic lights
    draw.ellipse([20, button_y - 8, 36, button_y + 8], fill="#ff6058")
    draw.ellipse([44, button_y - 8, 60, button_y + 8], fill="#ffbe2e")
    draw.ellipse([68, button_y - 8, 84, button_y + 8], fill="#2aca44")

    # Title
    title = window_title or f"{language.capitalize()} Code"
    font = load_font(font_family, 14, "medium")
    title_bbox = draw.textbbox((0, 0), title, font=font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = frame_width // 2 - title_width // 2
    draw.text((title_x, button_y - 8), title, fill="#ffffff", font=font)

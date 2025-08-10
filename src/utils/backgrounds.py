"""Background generation utilities."""

from PIL import Image, ImageDraw, ImageFilter
from config.constants import BACKGROUND_COLORS


def create_solid_background(width: int, height: int, color_name: str) -> Image.Image:
    """Create solid color backgrounds."""
    color = BACKGROUND_COLORS.get(color_name, color_name)
    return Image.new("RGB", (width, height), color)


def create_neon_background(width: int, height: int) -> Image.Image:
    """Create neon-style background with grid pattern."""
    img = Image.new("RGB", (width, height), "#000000")
    draw_bg = ImageDraw.Draw(img)
    
    grid_spacing = 50
    neon_color = "#00ff41"
    
    # Vertical lines
    for x in range(0, width, grid_spacing):
        draw_bg.line([(x, 0), (x, height)], fill=neon_color, width=1)
    
    # Horizontal lines
    for y in range(0, height, grid_spacing):
        draw_bg.line([(0, y), (width, y)], fill=neon_color, width=1)
    
    return img.filter(ImageFilter.GaussianBlur(radius=2))


def create_frame_background(frame_width: int, frame_height: int, background: str) -> Image.Image:
    """Create the appropriate background based on the background parameter."""
    if background == "transparent":
        return Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
    elif background.startswith("gradient-"):
        gradient_type = background.split("-")[1]
        if gradient_type == "purple":
            return Image.new("RGB", (frame_width, frame_height), "#8B5CF6")
        else:
            return create_solid_background(frame_width, frame_height, "purple")
    elif background.startswith("neon-"):
        return create_neon_background(frame_width, frame_height)
    elif background in BACKGROUND_COLORS:
        return create_solid_background(frame_width, frame_height, background)
    else:
        # Solid color or hex
        bg_color = background if background.startswith("#") else "#1a1a2e"
        return Image.new("RGB", (frame_width, frame_height), bg_color)

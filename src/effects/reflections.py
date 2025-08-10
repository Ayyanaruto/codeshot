"""Reflection effects for code screenshots."""

from PIL import Image, ImageDraw, ImageFilter
from PIL.Image import Transpose


def apply_reflection_effect(
    frame_img: Image.Image, 
    code_img: Image.Image, 
    code_x: int, 
    code_y: int
) -> Image.Image:
    """Add high-quality reflection effect."""
    reflection_img = code_img.copy()
    reflection_img = reflection_img.transpose(Transpose.FLIP_TOP_BOTTOM)
    
    # Create smooth gradient fade
    fade = Image.new("RGBA", reflection_img.size, (0, 0, 0, 0))
    fade_draw = ImageDraw.Draw(fade)
    
    reflection_height = reflection_img.height
    for y in range(reflection_height):
        ratio = y / reflection_height
        fade_ratio = 1 - (1 - ratio) ** 2  # Ease-out curve
        alpha = int(255 * (1 - fade_ratio) * 0.4)  # Max 40% opacity
        fade_draw.line([(0, y), (reflection_img.width, y)], fill=(0, 0, 0, 255 - alpha))
    
    reflection_img = reflection_img.convert("RGBA")
    reflection_img = Image.alpha_composite(reflection_img, fade)
    
    # Apply slight blur for realism
    reflection_img = reflection_img.filter(ImageFilter.GaussianBlur(radius=1))
    
    # Paste reflection
    reflection_y = code_y + code_img.height + 15
    if frame_img.mode != "RGBA":
        frame_img = frame_img.convert("RGBA")
    frame_img.paste(reflection_img, (code_x, reflection_y), reflection_img)
    
    return frame_img

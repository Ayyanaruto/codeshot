"""Border glow and other special effects."""

from PIL import Image, ImageDraw, ImageFilter


def apply_border_glow(frame_img: Image.Image, frame_width: int, frame_height: int) -> Image.Image:
    """Apply simple glowing border effect."""
    glow_color = "#00ff41"
    r, g, b = tuple(int(glow_color[i:i+2], 16) for i in (1, 3, 5))
    
    if frame_img.mode != "RGBA":
        frame_img = frame_img.convert("RGBA")
    
    glow_layer_img = Image.new("RGBA", (frame_width, frame_height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer_img)
    glow_draw.rectangle([5, 5, frame_width-5, frame_height-5], outline=(r, g, b, 100), width=3)
    glow_layer_img = glow_layer_img.filter(ImageFilter.GaussianBlur(radius=3))
    
    return Image.alpha_composite(frame_img, glow_layer_img)


def apply_rounded_corners(code_img: Image.Image, radius: int = 12) -> Image.Image:
    """Apply high-quality rounded corners with anti-aliasing."""
    mask_scale = 4  # Higher resolution for smoother curves
    mask_size = (code_img.width * mask_scale, code_img.height * mask_scale)
    mask = Image.new("L", mask_size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([0, 0, mask_size[0], mask_size[1]], radius=radius*mask_scale, fill=255)
    
    # Scale down with high-quality resampling
    mask = mask.resize(code_img.size, Image.Resampling.LANCZOS)
    
    # Apply mask
    code_img = code_img.convert("RGBA")
    code_img.putalpha(mask)
    
    return code_img


def add_watermark(
    frame_img: Image.Image, 
    watermark_text: str, 
    font, 
    frame_width: int, 
    frame_height: int
) -> Image.Image:
    """Add watermark to the image."""
    watermark_draw = ImageDraw.Draw(frame_img)
    bbox = watermark_draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Position in bottom-right corner
    watermark_x = frame_width - text_width - 20
    watermark_y = frame_height - text_height - 20
    
    # Add semi-transparent background
    padding = 8
    bg_x1 = watermark_x - padding
    bg_y1 = watermark_y - padding
    bg_x2 = watermark_x + text_width + padding
    bg_y2 = watermark_y + text_height + padding
    
    watermark_draw.rounded_rectangle(
        [bg_x1, bg_y1, bg_x2, bg_y2],
        radius=6,
        fill=(0, 0, 0, 100)
    )
    
    # Draw watermark text
    watermark_draw.text((watermark_x, watermark_y), watermark_text, fill=(255, 255, 255, 200), font=font)
    
    return frame_img

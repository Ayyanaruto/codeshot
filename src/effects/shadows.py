"""Shadow effects for code screenshots."""

from PIL import Image, ImageDraw, ImageFilter

from config.constants import SHADOW_LAYERS


def create_simple_shadow(
    base_img: Image.Image,
    code_img: Image.Image,
    x: int,
    y: int,
    offset_x: int = 8,
    offset_y: int = 8,
    blur_radius: int = 20,
    opacity: float = 0.3,
    rounded_corners: bool = True,
) -> Image.Image:
    """Create simple shadow effects."""
    shadow_img = Image.new("RGBA", base_img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)

    shadow_x = x + offset_x
    shadow_y = y + offset_y
    shadow_color = (0, 0, 0, int(255 * opacity))

    if rounded_corners:
        shadow_draw.rounded_rectangle(
            [shadow_x, shadow_y, shadow_x + code_img.width, shadow_y + code_img.height],
            radius=15,
            fill=shadow_color,
        )
    else:
        shadow_draw.rectangle(
            [shadow_x, shadow_y, shadow_x + code_img.width, shadow_y + code_img.height],
            fill=shadow_color,
        )

    return shadow_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))


def apply_shadow_effect(
    frame_img: Image.Image,
    code_img: Image.Image,
    code_x: int,
    code_y: int,
    rounded_corners: bool = True,
) -> Image.Image:
    """Apply layered shadow effect for realistic depth."""
    if frame_img.mode != "RGBA":
        frame_img = frame_img.convert("RGBA")

    for layer in SHADOW_LAYERS:
        shadow_layer = create_simple_shadow(
            frame_img,
            code_img,
            code_x,
            code_y,
            offset_x=layer["offset"][0],
            offset_y=layer["offset"][1],
            blur_radius=layer["blur"],
            opacity=layer["opacity"],
            rounded_corners=rounded_corners,
        )
        frame_img = Image.alpha_composite(frame_img, shadow_layer)

    return frame_img

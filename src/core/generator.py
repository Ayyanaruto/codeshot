"""Main codeshot generation orchestrator."""

import base64
import io
from typing import List, Optional

from PIL import Image, ImageDraw

from config.constants import EXTRA_SPACE, PADDING, TITLE_BAR_HEIGHT
from config.logging_config import get_logger, log_performance
from src.core.renderer import create_code_image, detect_language
from src.effects.reflections import apply_reflection_effect
from src.effects.shadows import apply_shadow_effect
from src.effects.special import add_watermark, apply_border_glow, apply_rounded_corners
from src.frames.macos import draw_macos_frame
from src.frames.windows import draw_windows_frame
from src.utils.backgrounds import create_frame_background
from src.utils.fonts import load_font
from src.utils.validation import (
    ValidationResult,
    format_response_text,
    validate_background,
    validate_boolean_with_random,
    validate_font_family,
    validate_font_size,
    validate_frame_style,
    validate_string_optional,
    validate_theme,
)


class CodeshotGenerator:
    """Main class for generating code screenshots."""

    def __init__(self):
        self.validation_result = ValidationResult()
        self.logger = get_logger(__name__)
        self.logger.debug("CodeshotGenerator initialized")

    def generate(
        self,
        code: str,
        language: Optional[str] = None,
        theme: Optional[str] = None,
        frame_style: Optional[str] = None,
        background: Optional[str] = None,
        font_family: Optional[str] = None,
        font_size: Optional[int] = None,
        line_numbers: bool = True,
        window_title: Optional[str] = None,
        shadow: Optional[bool] = None,
        reflection: bool = False,
        rounded_corners: Optional[bool] = None,
        watermark: Optional[str] = None,
        border_glow: Optional[bool] = None,
    ) -> tuple[str, str]:  # Returns (response_text, base64_image)
        """Generate a code screenshot with the specified parameters."""

        with log_performance(self.logger, "screenshot generation"):
            self.logger.info("Starting code screenshot generation")
            self.logger.debug(f"Code length: {len(code)} characters")

            # Validate all parameters
            self.logger.debug("Validating input parameters")
            theme = validate_theme(theme, self.validation_result)
            frame_style = validate_frame_style(frame_style, self.validation_result)
            background = validate_background(background, self.validation_result)
            font_family = validate_font_family(font_family, self.validation_result)
            font_size = validate_font_size(font_size, self.validation_result)

            shadow = validate_boolean_with_random(shadow, "Shadow", True, self.validation_result)
            rounded_corners = validate_boolean_with_random(
                rounded_corners, "Rounded Corners", True, self.validation_result
            )
            border_glow = validate_boolean_with_random(
                border_glow, "Border Glow", False, self.validation_result, 0.2
            )

            window_title = validate_string_optional(window_title, "Window Title")
            watermark = validate_string_optional(watermark, "Watermark")

            self.logger.info(
                f"Final parameters: theme={theme}, frame={frame_style}, background={background}, font={font_family}, size={font_size}"
            )

            # Detect language
            self.logger.debug("Detecting programming language")
            language = detect_language(code, language)
            self.logger.info(f"Detected language: {language}")

            # Get font path
            font_path = None
            try:
                from fonts import get_font_path

                if font_family != "system":
                    font_path_obj = get_font_path(font_family, "regular")
                    if font_path_obj:
                        font_path = str(font_path_obj)
                        self.logger.debug(f"Using font path: {font_path}")
            except ImportError:
                self.logger.debug("Font module not available, using system fonts")
                pass

            # Create code image
            self.logger.debug("Creating code image with syntax highlighting")
            code_img = create_code_image(code, language, theme, font_size, line_numbers, font_path)
            self.logger.debug(f"Code image dimensions: {code_img.width}x{code_img.height}")

            # Apply rounded corners to code image
            if rounded_corners:
                self.logger.debug("Applying rounded corners to code image")
                code_img = apply_rounded_corners(code_img)

            # Calculate frame dimensions
            title_bar_height = TITLE_BAR_HEIGHT if frame_style != "none" else 0
            extra_space = EXTRA_SPACE if shadow or reflection else 20

            frame_width = code_img.width + (PADDING * 2) + extra_space
            frame_height = code_img.height + (PADDING * 2) + title_bar_height + extra_space

            if reflection:
                frame_height += code_img.height // 2

            self.logger.debug(f"Frame dimensions: {frame_width}x{frame_height}")

            # Create frame background
            self.logger.debug("Creating frame background")
            frame_img = create_frame_background(frame_width, frame_height, background)
            draw = ImageDraw.Draw(frame_img)

            # Calculate code position
            code_x = PADDING + (extra_space // 2)
            code_y = title_bar_height + PADDING

            # Draw window frame
            if frame_style == "macos":
                self.logger.debug("Drawing macOS window frame")
                draw_macos_frame(
                    draw, frame_width, title_bar_height, window_title, language, font_family
                )
            elif frame_style == "windows":
                self.logger.debug("Drawing Windows window frame")
                draw_windows_frame(
                    draw, frame_width, title_bar_height, window_title, language, font_family
                )

            # Apply shadow effect
            if shadow and frame_style != "none":
                self.logger.debug("Applying shadow effect")
                frame_img = apply_shadow_effect(
                    frame_img, code_img, code_x, code_y, rounded_corners
                )

            # Paste code image
            self.logger.debug("Pasting code image onto frame")
            frame_img.paste(
                code_img, (int(code_x), int(code_y)), code_img if rounded_corners else None
            )

            # Apply reflection effect
            if reflection:
                self.logger.debug("Applying reflection effect")
                frame_img = apply_reflection_effect(frame_img, code_img, code_x, code_y)

            # Apply border glow
            if border_glow:
                self.logger.debug("Applying border glow effect")
                frame_img = apply_border_glow(frame_img, frame_width, frame_height)

            # Add watermark
            if watermark:
                self.logger.debug(f"Adding watermark: {watermark}")
                watermark_font = load_font(font_family, 12, "regular")
                frame_img = add_watermark(
                    frame_img, watermark, watermark_font, frame_width, frame_height
                )

            # Convert to base64
            self.logger.debug("Converting image to base64")
            buf = io.BytesIO()
            if background == "transparent":
                frame_img.save(buf, format="PNG", optimize=True)
            else:
                if frame_img.mode == "RGBA":
                    rgb_img = Image.new("RGB", frame_img.size, "#ffffff")
                    rgb_img.paste(frame_img, mask=frame_img.split()[-1])
                    frame_img = rgb_img
                frame_img.save(buf, format="PNG", optimize=True)

            img_bytes = buf.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode("utf-8")
            self.logger.debug(f"Generated base64 image: {len(img_base64)} characters")

            # Generate response text
            effects = []
            if shadow:
                effects.append("Shadow")
            if reflection:
                effects.append("Reflection")
            if border_glow:
                effects.append("Glow")
            if rounded_corners:
                effects.append("Rounded")

            response_text = format_response_text(
                language,
                theme,
                frame_style,
                background,
                font_family,
                font_size,
                frame_width,
                frame_height,
                effects,
                self.validation_result,
            )

            self.logger.info("Screenshot generation completed successfully")
            return response_text, img_base64

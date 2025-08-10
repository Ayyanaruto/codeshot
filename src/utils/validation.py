"""Utility functions for parameter validation and random selection."""

import random
from typing import Any, List, Optional, Tuple, Union

from config.constants import (
    AVAILABLE_BACKGROUNDS,
    AVAILABLE_FONTS,
    AVAILABLE_FRAMES,
    AVAILABLE_THEMES,
    DEFAULT_FONT_SIZE_RANGE,
    FONT_SIZE_LIMITS,
)
from config.logging_config import get_logger

# Module logger
logger = get_logger(__name__)


class ValidationResult:
    """Result of parameter validation with random selections and fallback notifications."""

    def __init__(self):
        self.random_selections: List[str] = []
        self.fallback_notifications: List[str] = []


def validate_theme(theme: Optional[str], result: ValidationResult) -> str:
    """Validate and handle theme parameter."""
    if theme is None:
        theme = random.choice(AVAILABLE_THEMES)
        result.random_selections.append("Theme")
        logger.debug(f"Randomly selected theme: {theme}")
    elif theme not in AVAILABLE_THEMES:
        result.fallback_notifications.append(f"Invalid theme '{theme}', using 'dracula'")
        logger.warning(f"Invalid theme '{theme}', falling back to 'dracula'")
        theme = "dracula"
    else:
        logger.debug(f"Using specified theme: {theme}")
    return theme


def validate_frame_style(frame_style: Optional[str], result: ValidationResult) -> str:
    """Validate and handle frame style parameter."""
    if frame_style is None:
        frame_style = random.choice(AVAILABLE_FRAMES)
        result.random_selections.append("Frame")
        logger.debug(f"Randomly selected frame style: {frame_style}")
    elif frame_style not in AVAILABLE_FRAMES:
        result.fallback_notifications.append(f"Invalid frame style '{frame_style}', using 'macos'")
        logger.warning(f"Invalid frame style '{frame_style}', falling back to 'macos'")
        frame_style = "macos"
    else:
        logger.debug(f"Using specified frame style: {frame_style}")
    return frame_style


def validate_background(background: Optional[str], result: ValidationResult) -> str:
    """Validate and handle background parameter."""
    if background is None:
        background = random.choice(AVAILABLE_BACKGROUNDS)
        result.random_selections.append("Background")
        logger.debug(f"Randomly selected background: {background}")
    elif background not in AVAILABLE_BACKGROUNDS and not _is_valid_hex_color(background):
        result.fallback_notifications.append(f"Invalid background '{background}', using 'purple'")
        logger.warning(f"Invalid background '{background}', falling back to 'purple'")
        background = "purple"
    else:
        logger.debug(f"Using specified background: {background}")
    return background


def validate_font_family(font_family: Optional[str], result: ValidationResult) -> str:
    """Validate and handle font family parameter."""
    if font_family is None:
        font_family = random.choice(AVAILABLE_FONTS)
        result.random_selections.append("Font")
    elif font_family not in AVAILABLE_FONTS:
        result.fallback_notifications.append(
            f"Invalid font family '{font_family}', using 'fira-code'"
        )
        font_family = "fira-code"
    return font_family


def validate_font_size(font_size: Optional[int], result: ValidationResult) -> int:
    """Validate and handle font size parameter."""
    if font_size is None:
        font_size = random.randint(*DEFAULT_FONT_SIZE_RANGE)
        result.random_selections.append("Font Size")
    elif (
        not isinstance(font_size, int)
        or font_size < FONT_SIZE_LIMITS[0]
        or font_size > FONT_SIZE_LIMITS[1]
    ):
        result.fallback_notifications.append(f"Invalid font size '{font_size}', using 14")
        font_size = 14
    return font_size


def validate_boolean_with_random(
    value: Any, param_name: str, default: bool, result: ValidationResult, random_weight: float = 0.5
) -> bool:
    """Validate boolean parameters with optional random selection."""
    if value is None:
        value = random.choices([True, False], weights=[random_weight, 1 - random_weight])[0]
        if value:
            result.random_selections.append(param_name)
    elif not isinstance(value, bool):
        result.fallback_notifications.append(
            f"Invalid {param_name.lower()} value '{value}', using {default}"
        )
        value = default
    return value


def validate_string_optional(value: Any, param_name: str) -> Union[str, None]:
    """Validate optional string parameters."""
    if value is not None and not isinstance(value, str):
        return None
    return value


def _is_valid_hex_color(color: str) -> bool:
    """Check if a string is a valid hex color."""
    return (
        color.startswith("#")
        and len(color) in [4, 7]
        and all(c in "0123456789abcdefABCDEF" for c in color[1:])
    )


def format_response_text(
    language: str,
    theme: str,
    frame_style: str,
    background: str,
    font_family: str,
    font_size: int,
    frame_width: int,
    frame_height: int,
    effects: List[str],
    result: ValidationResult,
) -> str:
    """Format the response text with all the generation details."""
    effects_text = f" • Effects: {', '.join(effects)}" if effects else ""
    random_text = (
        f" • Random: {', '.join(result.random_selections)} 🎲" if result.random_selections else ""
    )
    fallback_text = (
        f"\n⚠️ **Fallbacks Applied**: {'; '.join(result.fallback_notifications)}"
        if result.fallback_notifications
        else ""
    )

    return (
        f"🎨 **Code Screenshot Generated!**\n\n"
        f"**Language**: {language.capitalize()}\n"
        f"**Theme**: {theme.title()}\n"
        f"**Frame**: {frame_style.title()}\n"
        f"**Background**: {background.title()}\n"
        f"**Font**: {font_family.title()} ({font_size}px)\n"
        f"**Size**: {frame_width}×{frame_height}px{effects_text}{random_text}{fallback_text}\n\n"
        f"Perfect for sharing! 🚀"
    )

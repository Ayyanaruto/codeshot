"""
Font configuration for codeshot
"""
import os
from pathlib import Path

# Base fonts directory
FONTS_DIR = Path(__file__).parent

# Font families available
FONT_FAMILIES = {
    "fira-code": {
        "name": "Fira Code",
        "regular": FONTS_DIR / "FiraCode" / "FiraCode-Regular.ttf",
        "bold": FONTS_DIR / "FiraCode" / "FiraCode-Bold.ttf",
        "light": FONTS_DIR / "FiraCode" / "FiraCode-Light.ttf",
        "medium": FONTS_DIR / "FiraCode" / "FiraCode-Medium.ttf",
        "retina": FONTS_DIR / "FiraCode" / "FiraCode-Retina.ttf",
        "semibold": FONTS_DIR / "FiraCode" / "FiraCode-SemiBold.ttf",
        "variable": FONTS_DIR / "FiraCode" / "FiraCode-VF.ttf",
    },
    "jetbrains-mono": {
        "name": "JetBrains Mono",
        "regular": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Regular.ttf",
        "bold": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Bold.ttf",
        "light": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Light.ttf",
        "medium": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Medium.ttf",
        "semibold": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-SemiBold.ttf",
        "extrabold": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-ExtraBold.ttf",
        "thin": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Thin.ttf",
        "extralight": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-ExtraLight.ttf",
        "italic": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-Italic.ttf",
        "bold_italic": FONTS_DIR / "JetBrainsMono" / "JetBrainsMono-BoldItalic.ttf",
    },
    "source-code-pro": {
        "name": "Source Code Pro",
        "regular": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Regular.otf",
        "bold": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Bold.otf",
        "light": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Light.otf",
        "medium": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Medium.otf",
        "semibold": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Semibold.otf",
        "black": FONTS_DIR / "SourceCodePro" / "SourceCodePro-Black.otf",
        "extralight": FONTS_DIR / "SourceCodePro" / "SourceCodePro-ExtraLight.otf",
        "italic": FONTS_DIR / "SourceCodePro" / "SourceCodePro-It.otf",
        "bold_italic": FONTS_DIR / "SourceCodePro" / "SourceCodePro-BoldIt.otf",
    },
}

# Default font configurations
DEFAULT_CODE_FONT = "jetbrains-mono"
DEFAULT_UI_FONT = "source-code-pro"

# Font fallbacks (system fonts)
FALLBACK_FONTS = [
    "DejaVu Sans Mono",
    "Consolas", 
    "Monaco",
    "Lucida Console",
    "Liberation Mono",
    "Courier New",
    "monospace"
]

def get_font_path(family: str, weight: str = "regular") -> Path | None:
    """
    Get the path to a specific font file.
    
    Args:
        family: Font family name (e.g., 'fira-code', 'jetbrains-mono')
        weight: Font weight (e.g., 'regular', 'bold', 'light')
    
    Returns:
        Path to the font file, or None if not found
    """
    family_config = FONT_FAMILIES.get(family)
    if not family_config:
        return None
    
    font_path = family_config.get(weight)
    if font_path and font_path.exists():
        return font_path
    
    # Fallback to regular if weight not found
    regular_path = family_config.get("regular")
    if regular_path and regular_path.exists():
        return regular_path
    
    return None

def get_available_fonts() -> list[str]:
    """Get list of available font families."""
    return list(FONT_FAMILIES.keys())

def get_font_weights(family: str) -> list[str]:
    """Get available weights for a font family."""
    family_config = FONT_FAMILIES.get(family, {})
    return [k for k in family_config.keys() if k != "name"]

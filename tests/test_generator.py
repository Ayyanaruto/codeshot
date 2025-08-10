"""Test the core generator functionality."""

import base64
import io
from PIL import Image

from src.core.generator import CodeshotGenerator


def test_basic_generation(generator, sample_code):
    """Test basic code screenshot generation."""
    response_text, img_base64 = generator.generate(
        code=sample_code,
        theme="dracula",
        frame_style="macos",
        background="purple",
        font_family="fira-code",
        font_size=14,
        shadow=True,
        rounded_corners=True
    )
    
    # Check response text
    assert "Code Screenshot Generated" in response_text
    assert "Language: Python" in response_text
    assert "Theme: Dracula" in response_text
    
    # Check image is valid base64 and PNG
    assert img_base64
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))
    assert img.format == "PNG"
    assert img.width > 0
    assert img.height > 0


def test_random_generation(generator, sample_code):
    """Test generation with random parameters."""
    response_text, img_base64 = generator.generate(code=sample_code)
    
    # Should have random selections
    assert "Random:" in response_text
    assert img_base64  # Should still generate valid image


def test_validation_fallbacks(generator, sample_code):
    """Test parameter validation and fallbacks."""
    response_text, img_base64 = generator.generate(
        code=sample_code,
        theme="invalid_theme",
        frame_style="invalid_frame",
        background="invalid_background",
        font_family="invalid_font",
        font_size=999  # Invalid size
    )
    
    # Should have fallback notifications
    assert "Fallbacks Applied" in response_text
    assert img_base64  # Should still generate valid image

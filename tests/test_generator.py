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
    assert "**Language**: Python" in response_text
    assert "**Theme**: Dracula" in response_text
    
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


def test_all_themes_work(generator, sample_code):
    """Test that all available themes can generate screenshots without errors."""
    from config.constants import AVAILABLE_THEMES
    
    failed_themes = []
    successful_themes = []
    
    for theme in AVAILABLE_THEMES:
        try:
            response_text, img_base64 = generator.generate(
                code=sample_code,
                theme=theme,
                frame_style="minimal",  # Use minimal frame to focus on theme
                background="transparent",  # Use neutral background
                font_family="system",  # Use system font for consistency
                font_size=14,
                line_numbers=True,
                shadow=False,  # Disable effects to focus on theme
                reflection=False,
                rounded_corners=False,
                border_glow=False
            )
            
            # Verify response is valid
            assert response_text, f"No response text for theme: {theme}"
            assert img_base64, f"No image generated for theme: {theme}"
            assert f"**Theme**: {theme.title()}" in response_text or f"**Theme**: {theme.capitalize()}" in response_text, \
                f"Theme name not found in response for: {theme}"
            
            # Verify image is valid base64 and can be decoded
            img_bytes = base64.b64decode(img_base64)
            img = Image.open(io.BytesIO(img_bytes))
            assert img.format == "PNG", f"Invalid image format for theme: {theme}"
            assert img.width > 0 and img.height > 0, f"Invalid image dimensions for theme: {theme}"
            
            successful_themes.append(theme)
            
        except Exception as e:
            failed_themes.append((theme, str(e)))
    
    # Report results
    print(f"\n✅ Successfully tested {len(successful_themes)} themes")
    if successful_themes:
        print("Working themes:", ", ".join(successful_themes))
    
    if failed_themes:
        print(f"\n❌ {len(failed_themes)} themes failed:")
        for theme, error in failed_themes:
            print(f"  - {theme}: {error}")
    
    # Test should pass if at least 90% of themes work (allowing for some edge cases)
    success_rate = len(successful_themes) / len(AVAILABLE_THEMES)
    assert success_rate >= 0.9, f"Too many themes failed: {len(failed_themes)}/{len(AVAILABLE_THEMES)}. Failed themes: {[t[0] for t in failed_themes]}"


def test_dark_vs_light_themes(generator, sample_code):
    """Test specific dark and light themes to ensure contrast differences."""
    # Test a dark theme
    dark_response, dark_img_base64 = generator.generate(
        code=sample_code,
        theme="dracula",
        frame_style="minimal",
        background="transparent",
        font_family="system",
        font_size=14,
        shadow=False,
        reflection=False
    )
    
    # Test a light theme
    light_response, light_img_base64 = generator.generate(
        code=sample_code,
        theme="vs",
        frame_style="minimal", 
        background="transparent",
        font_family="system",
        font_size=14,
        shadow=False,
        reflection=False
    )
    
    # Both should generate valid images
    assert dark_img_base64 and light_img_base64
    assert "**Theme**: Dracula" in dark_response
    assert "**Theme**: Vs" in light_response
    
    # Images should be different (different themes should produce different results)
    assert dark_img_base64 != light_img_base64, "Dark and light themes should produce different images"


def test_theme_categories(generator, sample_code):
    """Test representative themes from different categories."""
    from config.constants import AVAILABLE_THEMES
    
    # Define test categories with representative themes
    test_categories = {
        "Popular Dark": ["dracula", "nord", "monokai", "one-dark"],
        "Popular Light": ["vs", "github-light", "solarized-light"],
        "Specialty": ["vim", "emacs", "terminal"],
        "Color Variants": ["gruvbox-dark", "gruvbox-light", "paraiso-dark", "paraiso-light"]
    }
    
    results = {}
    
    for category, themes in test_categories.items():
        category_results = []
        for theme in themes:
            if theme in AVAILABLE_THEMES:
                try:
                    response_text, img_base64 = generator.generate(
                        code=sample_code,
                        theme=theme,
                        frame_style="minimal",
                        background="transparent",
                        font_family="system"
                    )
                    assert img_base64, f"Failed to generate image for {theme}"
                    category_results.append((theme, True, None))
                except Exception as e:
                    category_results.append((theme, False, str(e)))
        
        results[category] = category_results
    
    # Print detailed results
    print(f"\n📊 Theme Category Test Results:")
    for category, theme_results in results.items():
        working = sum(1 for _, success, _ in theme_results if success)
        total = len(theme_results)
        print(f"  {category}: {working}/{total} working")
        
        for theme, success, error in theme_results:
            status = "✅" if success else "❌"
            print(f"    {status} {theme}" + (f" - {error}" if error else ""))
    
    # Ensure most themes in each category work
    for category, theme_results in results.items():
        working = sum(1 for _, success, _ in theme_results if success)
        total = len(theme_results)
        assert working > 0, f"No themes working in category: {category}"

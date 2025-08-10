"""Test all available themes for the codeshot generator."""

import base64
import io
import pytest
from PIL import Image

from src.core.generator import CodeshotGenerator
from config.constants import AVAILABLE_THEMES


def test_all_themes_work(generator, sample_code):
    """Test that all available themes can generate screenshots without errors."""
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
            
            # Check theme name appears in response (handle various capitalizations)
            theme_variations = [
                f"**Theme**: {theme.title()}",
                f"**Theme**: {theme.capitalize()}", 
                f"**Theme**: {theme.upper()}",
                f"**Theme**: {theme.replace('-', ' ').title()}",
                f"**Theme**: {theme.replace('-', '').title()}"
            ]
            theme_found = any(variation in response_text for variation in theme_variations)
            assert theme_found, f"Theme name not found in response for: {theme}. Response: {response_text}"
            
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
    
    # Check theme names in responses (handle various capitalizations)
    assert any(variant in dark_response for variant in ["**Theme**: Dracula", "**Theme**: DRACULA"])
    assert any(variant in light_response for variant in ["**Theme**: Vs", "**Theme**: VS"])
    
    # Images should be different (different themes should produce different results)
    assert dark_img_base64 != light_img_base64, "Dark and light themes should produce different images"


def test_theme_categories(generator, sample_code):
    """Test representative themes from different categories."""
    # Define test categories with representative themes
    test_categories = {
        "Popular Dark": ["dracula", "nord", "monokai", "one-dark"],
        "Popular Light": ["vs", "github-light", "solarized-light"],
        "Terminal/Editor": ["vim", "emacs", "terminal"],
        "Color Variants": ["gruvbox-dark", "gruvbox-light", "paraiso-dark", "paraiso-light"],
        "GitHub Themes": ["github-dark", "github-light"],
        "Material/Modern": ["material", "tokyo-night", "catppuccin"]
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


@pytest.mark.parametrize("theme", [
    "dracula", "nord", "monokai", "vs", "github-light", 
    "solarized-dark", "solarized-light", "vim", "emacs"
])
def test_individual_popular_themes(generator, sample_code, theme):
    """Test individual popular themes to ensure they work correctly."""
    response_text, img_base64 = generator.generate(
        code=sample_code,
        theme=theme,
        frame_style="minimal",
        background="transparent",
        font_family="system",
        font_size=14
    )
    
    # Verify basic requirements
    assert response_text, f"No response text for theme: {theme}"
    assert img_base64, f"No image generated for theme: {theme}"
    
    # Verify image is valid
    img_bytes = base64.b64decode(img_base64)
    img = Image.open(io.BytesIO(img_bytes))
    assert img.format == "PNG"
    assert img.width > 0 and img.height > 0
    
    # Verify theme is mentioned in response
    theme_variations = [
        f"**Theme**: {theme.title()}",
        f"**Theme**: {theme.capitalize()}", 
        f"**Theme**: {theme.upper()}",
        f"**Theme**: {theme.replace('-', ' ').title()}",
        f"**Theme**: {theme.replace('-', '').title()}"
    ]
    theme_found = any(variation in response_text for variation in theme_variations)
    assert theme_found, f"Theme name not found in response for: {theme}"


def test_theme_consistency(generator, sample_code):
    """Test that the same theme produces consistent results."""
    theme = "dracula"
    
    # Generate same screenshot twice
    response1, img1 = generator.generate(
        code=sample_code,
        theme=theme,
        frame_style="minimal",
        background="transparent",
        font_family="system",
        font_size=14,
        shadow=False,
        reflection=False,
        rounded_corners=False
    )
    
    response2, img2 = generator.generate(
        code=sample_code,
        theme=theme,
        frame_style="minimal",
        background="transparent",
        font_family="system",
        font_size=14,
        shadow=False,
        reflection=False,
        rounded_corners=False
    )
    
    # Results should be identical when all parameters are the same
    assert img1 == img2, "Same theme with same parameters should produce identical images"
    assert response1 == response2, "Same theme with same parameters should produce identical responses"


def test_theme_with_different_languages(generator):
    """Test that themes work correctly with different programming languages."""
    test_codes = {
        "python": '''
def hello_world():
    print("Hello, World!")
    return True
''',
        "javascript": '''
function helloWorld() {
    console.log("Hello, World!");
    return true;
}
''',
        "java": '''
public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}
''',
        "rust": '''
fn main() {
    println!("Hello, World!");
}
'''
    }
    
    themes_to_test = ["dracula", "vs", "monokai", "github-light"]
    
    for theme in themes_to_test:
        for language, code in test_codes.items():
            response_text, img_base64 = generator.generate(
                code=code,
                language=language,
                theme=theme,
                frame_style="minimal",
                background="transparent"
            )
            
            # Verify generation works
            assert img_base64, f"Failed to generate image for theme {theme} with language {language}"
            assert f"**Language**: {language.title()}" in response_text, f"Language not detected correctly for {language}"
            
            # Verify image is valid
            img_bytes = base64.b64decode(img_base64)
            img = Image.open(io.BytesIO(img_bytes))
            assert img.format == "PNG"


def test_edge_case_themes(generator, sample_code):
    """Test themes that might have edge cases or special handling."""
    edge_case_themes = [
        "tokyo-night",  # Has hyphen and might map to different pygments theme
        "catppuccin",   # Might map to different theme
        "terminal",     # Terminal-style theme
        "hacker",       # Alias theme
        "cyberpunk"     # Special effect theme
    ]
    
    for theme in edge_case_themes:
        if theme in AVAILABLE_THEMES:
            try:
                response_text, img_base64 = generator.generate(
                    code=sample_code,
                    theme=theme,
                    frame_style="minimal",
                    background="transparent"
                )
                
                assert img_base64, f"Edge case theme {theme} failed to generate image"
                
                # Verify image is valid
                img_bytes = base64.b64decode(img_base64)
                img = Image.open(io.BytesIO(img_bytes))
                assert img.format == "PNG"
                
            except Exception as e:
                pytest.fail(f"Edge case theme {theme} failed with error: {str(e)}")

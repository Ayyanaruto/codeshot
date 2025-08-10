"""Core code rendering functionality."""

import io
from typing import Optional
from PIL import Image, ImageFont
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name

from config.constants import THEME_MAPPINGS, QUALITY_SCALE


def detect_language(code: str, language: Optional[str] = None) -> str:
    """Auto-detect programming language if not specified."""
    if not language:
        try:
            # First, try to detect using common language patterns
            code_lower = code.lower()
            
            # Python hints
            python_hints = ['def ', 'import ', 'from ', 'class ', 'print(', '__init__', 'elif ', 'try:', 'except:', 'finally:', 'lambda ', 'with ', 'yield']
            python_score = sum(1 for hint in python_hints if hint in code_lower)
            
            # JavaScript hints  
            js_hints = ['function ', 'const ', 'let ', 'var ', 'console.log', '=>', 'return ', 'typeof', 'null', 'undefined']
            js_score = sum(1 for hint in js_hints if hint in code_lower)
            
            # Java hints
            java_hints = ['public class', 'private ', 'public ', 'static ', 'void main', 'system.out.println', 'string[]']
            java_score = sum(1 for hint in java_hints if hint in code_lower)
            
            # Rust hints
            rust_hints = ['fn ', 'let mut', 'match ', 'impl ', 'struct ', 'enum ', 'println!']
            rust_score = sum(1 for hint in rust_hints if hint in code_lower)
            
            # Use heuristic scoring
            scores = {
                'python': python_score,
                'javascript': js_score, 
                'java': java_score,
                'rust': rust_score
            }
            
            # If we have a clear winner, use it
            max_score = max(scores.values())
            if max_score >= 2:  # At least 2 hints
                detected = max(scores.keys(), key=lambda k: scores[k])
                return detected
            
            # Fall back to pygments guess_lexer
            lexer = guess_lexer(code.strip())
            detected_name = lexer.name.lower()
            
            # Map common lexer names to more recognizable ones
            name_mappings = {
                'tera term macro': 'python',  # Common misdetection
                'text': 'python',
                'common lisp': 'python' if python_score > 0 else 'text'
            }
            
            return name_mappings.get(detected_name, detected_name)
            
        except Exception:
            return "python"
    return language


def create_code_image(
    code: str, 
    language: str, 
    theme: str, 
    font_size: int, 
    line_numbers: bool = True,
    font_path: Optional[str] = None
) -> Image.Image:
    """Generate syntax highlighted code image."""
    # Get lexer
    try:
        lexer = get_lexer_by_name(language)
    except:
        lexer = get_lexer_by_name("text")
    
    # Map theme to pygments style
    pygments_theme = THEME_MAPPINGS.get(theme, theme)
    
    # Enhanced formatter with ultra-high-quality settings
    formatter_kwargs = {
        "style": pygments_theme,
        "font_size": font_size * QUALITY_SCALE,
        "line_numbers": line_numbers,
        "line_number_chars": 4,
        "line_number_pad": 15 * QUALITY_SCALE,
        "line_number_separator": True,
        "image_format": "PNG",
        "image_pad": 25 * QUALITY_SCALE,
        "image_quality": 100,
    }
    
    # Theme-specific styling
    if theme in ["dracula", "catppuccin"]:
        formatter_kwargs.update({
            "line_number_bg": "#1a1b26",
            "line_number_fg": "#565f89", 
            "hl_color": "#FFE066"         # Bright sunny yellow highlight
        })
    elif theme in ["one-dark", "hacker"]:
        formatter_kwargs.update({
            "line_number_bg": "#282c34",
            "line_number_fg": "#5c6370", 
            "hl_color": "#61dafb"         # Cyan blue highlight
        })
    elif theme == "nord":
        formatter_kwargs.update({
            "line_number_bg": "#2e3440",
            "line_number_fg": "#616e88",
            "hl_color": "#4ECDC4"         # Vibrant turquoise highlight
        })
    elif theme == "nord-darker":
        formatter_kwargs.update({
            "line_number_bg": "#1e222a",
            "line_number_fg": "#4c566a",
            "hl_color": "#88c0d0"         # Nord frost highlight
        })
    elif theme in ["gruvbox-dark", "tokyo-night"]:
        formatter_kwargs.update({
            "line_number_bg": "#282828",
            "line_number_fg": "#7c6f64",
            "hl_color": "#fabd2f"         # Golden yellow highlight
        })
    elif theme == "material":
        formatter_kwargs.update({
            "line_number_bg": "#263238",
            "line_number_fg": "#546e7a",
            "hl_color": "#ff5722"         # Material orange highlight
        })
    elif theme in ["github-dark", "terminal"]:
        formatter_kwargs.update({
            "line_number_bg": "#0d1117",
            "line_number_fg": "#6e7681",
            "hl_color": "#ffa657"         # GitHub orange highlight
        })
    elif theme == "solarized-dark":
        formatter_kwargs.update({
            "line_number_bg": "#002b36",
            "line_number_fg": "#586e75",
            "hl_color": "#2aa198"         # Solarized cyan highlight
        })
    elif theme == "zenburn":
        formatter_kwargs.update({
            "line_number_bg": "#3f3f3f",
            "line_number_fg": "#7f9f7f",
            "hl_color": "#dca3a3"         # Zenburn light pink highlight
        })
    elif theme in ["vim", "native"]:
        formatter_kwargs.update({
            "line_number_bg": "#000000",
            "line_number_fg": "#404040",
            "hl_color": "#00ff00"         # Classic terminal green highlight
        })
    elif theme in ["fruity", "cyberpunk"]:
        formatter_kwargs.update({
            "line_number_bg": "#111111",
            "line_number_fg": "#ffffff",
            "hl_color": "#ff0080"         # Hot pink cyberpunk highlight
        })
    elif theme == "rrt":
        formatter_kwargs.update({
            "line_number_bg": "#1e0010",
            "line_number_fg": "#ff0080",
            "hl_color": "#00ffff"         # Bright cyan highlight
        })
    elif theme in ["paraiso-dark", "stata-dark"]:
        formatter_kwargs.update({
            "line_number_bg": "#2f1e2e",
            "line_number_fg": "#776e71",
            "hl_color": "#ef6155"         # Paraiso red highlight
        })
    elif theme == "emacs":
        formatter_kwargs.update({
            "line_number_bg": "#000000",
            "line_number_fg": "#b2b2b2",
            "hl_color": "#00d4aa"         # Emacs teal highlight
        })
    elif theme in ["solarized-light", "github-light", "xcode", "intellij-light"]:
        formatter_kwargs.update({
            "line_number_bg": "#fafafa",
            "line_number_fg": "#93a1a1",
            "hl_color": "#268bd2"         # Solarized blue highlight
        })
    elif theme in ["vs", "atom-light", "sublime-light"]:
        formatter_kwargs.update({
            "line_number_bg": "#ffffff",
            "line_number_fg": "#2b91af",
            "hl_color": "#0000ff"         # Classic blue highlight
        })
    elif theme in ["friendly", "pastie", "colorful"]:
        formatter_kwargs.update({
            "line_number_bg": "#f8f8f8",
            "line_number_fg": "#888888",
            "hl_color": "#d73a49"         # GitHub red highlight
        })
    elif theme in ["tango", "murphy"]:
        formatter_kwargs.update({
            "line_number_bg": "#f5f5f5",
            "line_number_fg": "#666666",
            "hl_color": "#ff6347"         # Tomato red highlight
        })
    elif theme in ["gruvbox-light", "paraiso-light", "stata-light"]:
        formatter_kwargs.update({
            "line_number_bg": "#fbf1c7",
            "line_number_fg": "#7c6f64",
            "hl_color": "#af3a03"         # Gruvbox orange highlight
        })
    else:
        # Default dark theme styling
        formatter_kwargs.update({
            "line_number_bg": "#2d2d2d",
            "line_number_fg": "#8f8f8f", 
            "hl_color": "#FF6B9D"         # Bright pink highlight
        })
    
    if font_path:
        formatter_kwargs["font_name"] = font_path
    
    formatter = ImageFormatter(**formatter_kwargs)
    
    # Generate syntax highlighted image at high resolution
    highlighted_img_bytes = highlight(code, lexer, formatter)
    code_img_high_res = Image.open(io.BytesIO(highlighted_img_bytes))
    
    # Scale down with high-quality resampling
    target_width = code_img_high_res.width // QUALITY_SCALE
    target_height = code_img_high_res.height // QUALITY_SCALE
    code_img = code_img_high_res.resize(
        (target_width, target_height), 
        Image.Resampling.LANCZOS
    )
    
    return code_img

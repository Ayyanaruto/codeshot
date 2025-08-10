"""Configuration constants and mappings for the codeshot application."""

# Theme mappings for pygments
THEME_MAPPINGS = {
    # Dark themes
    "dracula": "dracula",
    "nord": "nord", 
    "monokai": "monokai",
    "material": "material",
    "one-dark": "one-dark",
    "gruvbox-dark": "gruvbox-dark",
    "tokyo-night": "monokai",
    "catppuccin": "dracula",
    "github-dark": "github-dark",
    "solarized-dark": "solarized-dark",
    "zenburn": "zenburn",
    "vim": "vim",
    "native": "native",
    "fruity": "fruity",
    "rrt": "rrt",
    "paraiso-dark": "paraiso-dark",
    "stata-dark": "stata-dark",
    "nord-darker": "nord-darker",
    "emacs": "emacs",
    "terminal": "native",
    "hacker": "vim",
    "cyberpunk": "fruity",
    
    # Light themes
    "solarized-light": "solarized-light", 
    "vs": "vs",
    "github-light": "default",
    "xcode": "default",
    "atom-light": "friendly",
    "intellij-light": "default",
    "sublime-light": "colorful",
    "friendly": "friendly",
    "pastie": "pastie",
    "tango": "tango",
    "murphy": "murphy",
    "colorful": "colorful",
    "gruvbox-light": "gruvbox-light",
    "paraiso-light": "paraiso-light",
    "stata-light": "stata-light",
}

# Available options for validation
AVAILABLE_THEMES = list(THEME_MAPPINGS.keys())
AVAILABLE_FRAMES = ["macos", "windows", "floating", "minimal", "none"]
AVAILABLE_BACKGROUNDS = [
    "purple", "cyan", "orange", "pink", "green", "blue", "red", "yellow",
    "magenta", "teal", "lime", "indigo", "violet", "coral", "turquoise",
    "neon-purple", "transparent",
    "#1a1a2e", "#16213e", "#0f3460", "#533483", "#7209b7", "#2d1b69",
    "#0c0c0c", "#1e1e1e", "#2d2d2d", "#3c3c3c", "#4a4a4a"
]
AVAILABLE_FONTS = ["fira-code", "jetbrains-mono", "source-code-pro", "system"]

# Color definitions for solid backgrounds
BACKGROUND_COLORS = {
    "purple": "#8B5CF6", "cyan": "#06B6D4", "orange": "#F97316", "pink": "#EC4899",
    "green": "#10B981", "blue": "#3B82F6", "red": "#EF4444", "yellow": "#F59E0B",
    "magenta": "#D946EF", "teal": "#14B8A6", "lime": "#84CC16", "indigo": "#6366F1",
    "violet": "#8B5CF6", "coral": "#FF6B6B", "turquoise": "#17A2B8",
}

# Quality and rendering settings
QUALITY_SCALE = 3  # 3x resolution for ultra-crisp text
DEFAULT_FONT_SIZE_RANGE = (12, 18)
FONT_SIZE_LIMITS = (8, 32)

# Effect settings
SHADOW_LAYERS = [
    {"offset": (15, 15), "blur": 30, "opacity": 0.4},
    {"offset": (8, 8), "blur": 18, "opacity": 0.3},
    {"offset": (4, 4), "blur": 10, "opacity": 0.25},
]

# Layout settings
PADDING = 80
TITLE_BAR_HEIGHT = 50
EXTRA_SPACE = 40

# Logging settings
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
DEFAULT_LOG_LEVEL = "INFO"
LOG_FILE_MAX_BYTES = 10 * 1024 * 1024  # 10MB
LOG_FILE_BACKUP_COUNT = 5

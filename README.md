# 🎨 Codeshot - Beautiful Code Screenshots

Generate stunning, professional code screenshots with themes, effects, and customizable styling. Perfect for social media, presentations, documentation, and sharing code snippets.

This project is built as a **Model Context Protocol (MCP) server**, enabling AI assistants to generate beautiful code screenshots programmatically.

## 🚢 Deployment

### Railway Deployment (Recommended)

This project is optimized for Railway deployment with Docker.

**Quick Deploy:**
1. Fork this repository
2. Connect to Railway
3. Set environment variables:
   - `AUTH_TOKEN` - Your authentication token
   - `MY_NUMBER` - Your phone number for authentication
   - `LOG_LEVEL` - Optional: DEBUG, INFO, WARNING, ERROR, CRITICAL (default: INFO)
4. Deploy!

**Included in Deployment:**
- ✅ All fonts bundled (Fira Code, JetBrains Mono, Source Code Pro)
- ✅ System dependencies (Tesseract, OpenCV, PIL)
- ✅ Production-ready Docker configuration
- ✅ Automatic environment detection

### Local Development

**Run locally:**
```bash
python main.py
```

**Docker Development:**
```bash
# Build the Docker image
docker build -t codeshot-mcp .

# Run with Docker
docker run -p 8086:8086 \
  -e AUTH_TOKEN=test \
  -e MY_NUMBER=123 \
  -e LOG_LEVEL=DEBUG \
  codeshot-mcp
```

**Docker Compose (Optional):**
```yaml
# docker-compose.yml
version: '3.8'
services:
  codeshot:
    build: .
    ports:
      - "8086:8086"
    environment:
      - AUTH_TOKEN=your-token
      - MY_NUMBER=your-number
      - LOG_LEVEL=INFO
```ippets.

## ✨ Features

- **🎨 Beautiful Themes**: Dracula, Nord, Monokai, GitHub Light, Material, and more
- **🖼️ Multiple Frame Styles**: macOS, Windows, Floating, Minimal, or no frame
- **🌈 Rich Backgrounds**: Solid colors, gradients, neon effects, or transparent
- **📝 Professional Typography**: Fira Code, JetBrains Mono, Source Code Pro fonts
- **✨ Visual Effects**: Shadows, reflections, rounded corners, border glow
- **🔗 URL Support**: Fetch code directly from GitHub, Gist, or any URL
- **🎲 Smart Randomization**: Automatic variety when parameters aren't specified
- **⚡ High Performance**: Optimized rendering with modular architecture

## 🚀 Quick Start

### System Requirements

- **Python 3.11+**
- **System Dependencies**: 
  - Tesseract OCR (for text processing)
  - OpenCV libraries
  - PIL/Pillow (Python Imaging Library)

**Note**: All dependencies are included in the Docker container for deployment.

### Installation

```bash
# Clone the repository
git clone https://github.com/Ayyanaruto/codeshot.git
cd codeshot

# Option 1: Install with pip
pip install -r requirements.txt

# Option 2: Install as package
pip install -e .

# Option 3: Install with uv (recommended)
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your AUTH_TOKEN and MY_NUMBER
```

### Usage

**Environment Setup:**
```bash
# Required environment variables
export AUTH_TOKEN="your-secret-token"
export MY_NUMBER="your-phone-number"

# Optional: Set log level
export LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

**Start the Server:**
```bash
# Start the MCP server
python main.py
```

### MCP Tools Available

This server provides two main tools:

1. **`codeshot`** - Generate beautiful code screenshots with extensive customization options
2. **`validate`** - Validate configuration and check server status

### API Example

```python
# Generate a code screenshot
response = await codeshot(
    code='''
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
    ''',
    theme="dracula",
    frame_style="macos",
    background="purple",
    font_family="fira-code",
    shadow=True,
    rounded_corners=True
)

# Or fetch code from a URL
response = await codeshot(
    code_url="https://github.com/Ayyanaruto/codeshot/blob/main/main.py",
    theme="nord",
    frame_style="windows",
    background="transparent"
)
```

## 📁 Project Structure

```
codeshot/
├── main.py                 # MCP server entry point
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project configuration
├── uv.lock               # Dependency lock file
├── Dockerfile            # Docker container configuration
├── railway.json          # Railway deployment config
├── start.sh             # Production startup script
├── .env.example         # Environment variables template
├── config/              # Configuration and constants
│   ├── __init__.py
│   ├── constants.py      # Theme mappings, color definitions
│   └── logging_config.py # Logging setup
├── src/                 # Core application code
│   ├── __init__.py
│   ├── core/            # Core functionality
│   │   ├── __init__.py
│   │   ├── generator.py  # Main screenshot generator
│   │   └── renderer.py   # Code rendering logic
│   ├── utils/           # Utility functions
│   │   ├── __init__.py
│   │   ├── validation.py # Parameter validation
│   │   ├── fonts.py      # Font loading utilities
│   │   ├── http.py       # URL fetching
│   │   └── backgrounds.py # Background generation
│   ├── effects/         # Visual effects
│   │   ├── __init__.py
│   │   ├── shadows.py    # Shadow effects
│   │   ├── reflections.py # Reflection effects
│   │   └── special.py    # Glow, watermarks, etc.
│   └── frames/          # Window frame styles
│       ├── __init__.py
│       ├── macos.py      # macOS window frame
│       └── windows.py    # Windows window frame
├── fonts/               # Font assets
│   ├── FiraCode/
│   ├── JetBrainsMono/
│   └── SourceCodePro/
├── tests/               # Test suite
│   ├── conftest.py
│   ├── test_generator.py
│   └── test_themes.py
└── logs/               # Application logs
    └── codeshot.log
```

## 🎨 Themes

### Dark Themes
- **dracula** - Dark theme with purple accents
- **nord** - Arctic, north-bluish color palette  
- **monokai** - Classic dark theme with vibrant colors
- **material** - Google's Material Design dark
- **one-dark** - Atom's iconic One Dark theme
- **gruvbox-dark** - Retro groove color scheme
- **tokyo-night** - A clean, dark theme inspired by Tokyo's night
- **catppuccin** - Soothing pastel theme for night owls
- **github-dark** - GitHub's dark theme
- **solarized-dark** - Precision colors for machines and people
- **zenburn** - Low-contrast color scheme
- **vim** - Classic Vim color scheme
- **native** - Terminal-style theme
- **fruity** - Colorful syntax highlighting
- **cyberpunk** - High-contrast neon theme

### Light Themes  
- **github-light** - Clean light theme
- **solarized-light** - Precision colors for machines and people
- **vs** - Visual Studio light theme
- **friendly** - Easy on the eyes light theme
- **colorful** - Vibrant light theme
- **gruvbox-light** - Light version of the retro groove scheme

## 🖼️ Frame Styles

- **macos** - macOS window with traffic light buttons
- **windows** - Windows window with minimize/maximize/close
- **floating** - Clean floating frame
- **minimal** - Minimal border
- **none** - No frame, just code

## 🌈 Backgrounds

- **Solid Colors**: purple, cyan, orange, pink, green, blue, red, yellow, etc.
- **Hex Colors**: Any valid hex color code (#1a1a2e, #533483, etc.)
- **Special**: transparent, neon-purple (with grid effect)

## ⚙️ Configuration

The application uses a modular configuration system:

- **config/constants.py** - All theme mappings, colors, and settings
- **Environment Variables** - AUTH_TOKEN and MY_NUMBER for MCP auth
- **Font Configuration** - Automatic font loading with system fallbacks

## 🛠️ Development

### Code Quality Tools

```bash
# Format code
black src/ config/ main.py

# Sort imports
isort src/ config/ main.py

# Type checking
mypy src/ config/ main.py

# Linting
flake8 src/ config/ main.py

# Run tests
pytest
```

### Architecture

The codebase follows clean architecture principles:

- **Separation of Concerns**: Each module has a single responsibility
- **Dependency Injection**: Core components don't depend on utilities
- **Type Safety**: Full type annotations with mypy checking
- **Error Handling**: Comprehensive error handling with fallbacks
- **Modularity**: Easy to extend with new themes, effects, or frames

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_generator.py
```

## 📊 Logging and Monitoring

Codeshot includes a comprehensive logging system for debugging and monitoring:

### Quick Setup
```bash
# Set log level in environment
export LOG_LEVEL=DEBUG  # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Features
- **Colored Console Output**: Easy-to-read colored logs in terminal
- **Rotating Log Files**: Automatic log rotation (10MB max, 5 backups)
- **Performance Monitoring**: Built-in timing for operations
- **Module-Specific Logging**: Separate loggers for each component
- **Error Tracking**: Detailed error logging with stack traces

### Example Usage
```python
from config.logging_config import get_logger, log_performance

logger = get_logger(__name__)

# Basic logging
logger.info("Starting screenshot generation")
logger.debug("Processing parameters")
logger.error("Something went wrong")

# Performance monitoring
with log_performance(logger, "image generation"):
    generate_screenshot()
```

### Log Files
- Default location: `logs/codeshot.log`
- Automatic rotation when files exceed 10MB
- Configurable via `LOG_FILE` environment variable

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📧 Support

-  [Bug Reports](https://github.com/Ayyanaruto/codeshot/issues)
- 💬 [Discussions](https://github.com/Ayyanaruto/codeshot/discussions)

---

Made with ❤️ by Ayyan

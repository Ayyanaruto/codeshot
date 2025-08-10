#!/bin/bash

# Local test script for Codeshot MCP Server

echo "🧪 Testing Codeshot MCP Server locally..."

# Set test environment variables
export AUTH_TOKEN="test_token_123"
export MY_NUMBER="12345"
export PORT="8086"

echo "📋 Test configuration:"
echo "  - AUTH_TOKEN: ${AUTH_TOKEN}"
echo "  - MY_NUMBER: ${MY_NUMBER}"
echo "  - PORT: ${PORT}"

echo ""
echo "🐍 Testing Python dependencies..."

# Test Python imports
python3 -c "
import sys
print(f'✅ Python: {sys.version}')

try:
    import PIL
    print(f'✅ Pillow: {PIL.__version__}')
except ImportError as e:
    print(f'❌ Pillow: {e}')
    sys.exit(1)

try:
    import pygments
    print(f'✅ Pygments: {pygments.__version__}')
except ImportError as e:
    print(f'❌ Pygments: {e}')
    sys.exit(1)

try:
    import fastmcp
    print('✅ FastMCP: available')
except ImportError as e:
    print(f'❌ FastMCP: {e}')
    sys.exit(1)

try:
    import httpx
    print(f'✅ HTTPX: {httpx.__version__}')
except ImportError as e:
    print(f'❌ HTTPX: {e}')
    sys.exit(1)

try:
    import cv2
    print(f'✅ OpenCV: {cv2.__version__}')
except ImportError as e:
    print(f'❌ OpenCV: {e}')
    sys.exit(1)

print('✅ All dependencies are available')
"

echo ""
echo "🔤 Testing fonts..."
if [ -d "fonts" ]; then
    echo "✅ Fonts directory exists"
    echo "  📁 Font families found:"
    for font_dir in fonts/*/; do
        if [ -d "$font_dir" ]; then
            font_name=$(basename "$font_dir")
            font_count=$(find "$font_dir" -name "*.ttf" -o -name "*.otf" | wc -l)
            echo "    - $font_name ($font_count files)"
        fi
    done
else
    echo "❌ Fonts directory not found"
    exit 1
fi

echo ""
echo "🏗️ Testing import paths..."
python3 -c "
import sys
sys.path.insert(0, '.')

try:
    from src.core.generator import CodeshotGenerator
    print('✅ CodeshotGenerator import successful')
except ImportError as e:
    print(f'❌ CodeshotGenerator import failed: {e}')
    sys.exit(1)

try:
    from config.logging_config import setup_logging
    print('✅ Logging config import successful')
except ImportError as e:
    print(f'❌ Logging config import failed: {e}')
    sys.exit(1)

try:
    from fonts.config import FONT_FAMILIES
    print(f'✅ Font config import successful ({len(FONT_FAMILIES)} font families)')
except ImportError as e:
    print(f'❌ Font config import failed: {e}')
    sys.exit(1)
"

echo ""
echo "✅ All tests passed! Ready for deployment."
echo ""
echo "🚀 To deploy to Railway:"
echo "1. Set environment variables: AUTH_TOKEN, MY_NUMBER"
echo "2. Connect your GitHub repo to Railway"
echo "3. Deploy automatically with Docker"
echo ""
echo "📚 See DEPLOYMENT_CHECKLIST.md for detailed instructions"

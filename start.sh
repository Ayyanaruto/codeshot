#!/bin/bash

# Railway startup script for Codeshot MCP Server

echo "🚀 Starting Codeshot MCP Server..."
echo "📦 Version: $(cat VERSION 2>/dev/null || echo 'unknown')"
echo "🐍 Python: $(python --version)"
echo "🔧 Environment:"
echo "  - PORT: ${PORT:-8086}"
echo "  - LOG_LEVEL: ${LOG_LEVEL:-INFO}"
echo "  - AUTH_TOKEN: ${AUTH_TOKEN:+[SET]} ${AUTH_TOKEN:-[NOT_SET]}"
echo "  - MY_NUMBER: ${MY_NUMBER:+[SET]} ${MY_NUMBER:-[NOT_SET]}"

# Verify required environment variables
if [ -z "$AUTH_TOKEN" ]; then
    echo "❌ ERROR: AUTH_TOKEN environment variable is required"
    exit 1
fi

if [ -z "$MY_NUMBER" ]; then
    echo "❌ ERROR: MY_NUMBER environment variable is required"
    exit 1
fi

# Check if fonts are available
echo "🔤 Checking fonts..."
if [ -d "/app/fonts" ]; then
    echo "  ✅ Fonts directory found"
    ls -la /app/fonts/ | head -5
else
    echo "  ⚠️  Fonts directory not found"
fi

# Check Python dependencies
echo "📚 Checking key dependencies..."
python -c "import PIL; print(f'  ✅ Pillow: {PIL.__version__}')" 2>/dev/null || echo "  ❌ Pillow not found"
python -c "import pygments; print(f'  ✅ Pygments: {pygments.__version__}')" 2>/dev/null || echo "  ❌ Pygments not found"
python -c "import fastmcp; print('  ✅ FastMCP: available')" 2>/dev/null || echo "  ❌ FastMCP not found"

echo ""
echo "🏃 Starting server..."
exec python main.py

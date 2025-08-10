"""Main MCP server entry point."""

import asyncio
import os
from typing import Annotated, cast
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.server.auth.providers.bearer import BearerAuthProvider, RSAKeyPair
from mcp import ErrorData, McpError
from mcp.server.auth.provider import AccessToken
from mcp.types import TextContent, ImageContent, INVALID_PARAMS, INTERNAL_ERROR
from pydantic import BaseModel, Field, AnyUrl

from src.core.generator import CodeshotGenerator
from src.utils.http import fetch_code_from_url
from config.logging_config import setup_logging, get_logger

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

TOKEN = os.environ.get("AUTH_TOKEN")
MY_NUMBER = os.environ.get("MY_NUMBER")

assert TOKEN is not None, "Please set AUTH_TOKEN in your .env file"
assert MY_NUMBER is not None, "Please set MY_NUMBER in your .env file"

logger.info("Environment variables loaded successfully")


class SimpleBearerAuthProvider(BearerAuthProvider):
    """Simple bearer auth provider for MCP server."""
    
    def __init__(self, token: str):
        k = RSAKeyPair.generate()
        super().__init__(public_key=k.public_key, jwks_uri=None, issuer=None, audience=None)
        self.token = token
        self.logger = get_logger(__name__)
        self.logger.debug("SimpleBearerAuthProvider initialized")

    async def load_access_token(self, token: str) -> AccessToken | None:
        self.logger.debug(f"Loading access token for authentication")
        if token == self.token:
            self.logger.info("Authentication successful")
            return AccessToken(
                token=token,
                client_id="codeshot-client",
                scopes=["*"],
                expires_at=None,
            )
        self.logger.warning("Authentication failed - invalid token")
        return None


class RichToolDescription(BaseModel):
    """Rich tool description model."""
    description: str
    use_when: str
    side_effects: str | None = None


# MCP Server Setup
mcp = FastMCP(
    "Codeshot MCP Server",
    auth=SimpleBearerAuthProvider(TOKEN),
)

logger.info("MCP server initialized with authentication")


@mcp.tool
async def validate() -> str:
    """Validation tool required by Puch."""
    logger.debug("Validation tool called")
    return cast(str, MY_NUMBER)


CODESHOT_DESCRIPTION = RichToolDescription(
    description=(
        "Generate beautiful code screenshots with themes, colors, and frame styles. "
        "Features solid backgrounds, GitHub/Gist URL support, shadows, reflections, and effects. "
        "Automatically selects random themes, frames, backgrounds, and fonts when not specified for variety and surprise. "
        "Perfect for social media, presentations, and documentation."
    ),
    use_when="Use when you need beautiful code images for sharing, presentations, or social media.",
    side_effects=None,
)


@mcp.tool(description=CODESHOT_DESCRIPTION.model_dump_json())
async def codeshot(
    code: Annotated[str | None, Field(description="Raw code text to convert to image")] = None,
    code_url: Annotated[AnyUrl | None, Field(description="GitHub/Gist URL to fetch code from")] = None,
    from_image: Annotated[bool, Field(description="Whether to generate from an existing image (for compatibility)")] = False,
    language: Annotated[str | None, Field(description="Programming language (auto-detected if not specified)")] = None,
    theme: Annotated[str | None, Field(description="Theme: Dark themes: 'dracula', 'nord', 'monokai', 'material', 'one-dark', 'gruvbox-dark', 'tokyo-night', 'catppuccin', 'github-dark', 'solarized-dark', 'zenburn', 'vim', 'native', 'fruity', 'rrt', 'paraiso-dark', 'stata-dark', 'nord-darker', 'emacs', 'terminal', 'hacker', 'cyberpunk'. Light themes: 'solarized-light', 'github-light', 'vs', 'xcode', 'atom-light', 'intellij-light', 'sublime-light', 'friendly', 'pastie', 'tango', 'murphy', 'colorful', 'gruvbox-light', 'paraiso-light', 'stata-light', or leave empty for random theme")] = None,
    frame_style: Annotated[str | None, Field(description="Frame: 'macos', 'windows', 'floating', 'minimal', 'none', or leave empty for random frame")] = None,
    background: Annotated[str | None, Field(description="Background: hex color, 'purple', 'cyan', 'orange', 'pink', 'green', 'blue', 'red', 'yellow', 'magenta', 'teal', 'lime', 'indigo', 'violet', 'coral', 'turquoise', 'neon-purple', 'transparent', or leave empty for random background")] = None,
    font_family: Annotated[str | None, Field(description="Font: 'fira-code', 'jetbrains-mono', 'source-code-pro', 'system', or leave empty for random font")] = None,
    font_size: Annotated[int | None, Field(description="Font size (8-32), or leave empty for random size")] = None,
    line_numbers: Annotated[bool, Field(description="Show line numbers")] = True,
    window_title: Annotated[str | None, Field(description="Custom window title")] = None,
    shadow: Annotated[bool | None, Field(description="Add drop shadow effect, or leave empty for random")] = None,
    reflection: Annotated[bool, Field(description="Add reflection effect")] = False,
    rounded_corners: Annotated[bool | None, Field(description="Rounded corners, or leave empty for random")] = None,
    watermark: Annotated[str | None, Field(description="Add watermark text")] = None,
    border_glow: Annotated[bool | None, Field(description="Add glowing border effect, or leave empty for random")] = None,
) -> list[TextContent | ImageContent]:
    """Generate stunning code screenshots with advanced themes, effects, and professional styling."""
    
    request_logger = get_logger(__name__)
    request_logger.info("Codeshot generation requested")
    request_logger.debug(f"Parameters: theme={theme}, frame_style={frame_style}, background={background}, font_family={font_family}")
    
    try:
        # Handle from_image parameter for compatibility
        if from_image:
            request_logger.warning("Image-based code generation attempted (not supported)")
            raise McpError(ErrorData(
                code=INVALID_PARAMS, 
                message="Image-based code generation is not currently supported. Please provide code text or a code URL instead."
            ))
        
        # Get code content
        if code_url:
            request_logger.info(f"Fetching code from URL: {code_url}")
            code_content = await fetch_code_from_url(str(code_url))
            request_logger.debug(f"Successfully fetched {len(code_content)} characters from URL")
        elif code:
            request_logger.info("Using provided code text")
            code_content = code
            request_logger.debug(f"Code length: {len(code_content)} characters")
        else:
            request_logger.error("No code source provided")
            raise McpError(ErrorData(
                code=INVALID_PARAMS, 
                message="Please provide either code text or a code URL."
            ))
        
        # Generate screenshot
        request_logger.info("Starting screenshot generation")
        generator = CodeshotGenerator()
        response_text, img_base64 = generator.generate(
            code=code_content,
            language=language,
            theme=theme,
            frame_style=frame_style,
            background=background,
            font_family=font_family,
            font_size=font_size,
            line_numbers=line_numbers,
            window_title=window_title,
            shadow=shadow,
            reflection=reflection,
            rounded_corners=rounded_corners,
            watermark=watermark,
            border_glow=border_glow,
        )
        
        request_logger.info("Screenshot generation completed successfully")
        request_logger.debug(f"Generated image size: {len(img_base64)} characters (base64)")
        
        return [
            TextContent(type="text", text=response_text),
            ImageContent(type="image", mimeType="image/png", data=img_base64)
        ]
        
    except McpError:
        # Re-raise MCP errors as-is
        raise
    except Exception as e:
        request_logger.error(f"Unexpected error during screenshot generation: {str(e)}", exc_info=True)
        raise McpError(ErrorData(
            code=INTERNAL_ERROR, 
            message=f"Failed to generate code screenshot: {str(e)}"
        ))


async def main():
    """Main entry point."""
    logger.info("🚀 Starting Codeshot MCP Server on http://0.0.0.0:8086")
    print("🚀 Starting Codeshot MCP Server on http://0.0.0.0:8086")
    try:
        await mcp.run_async("streamable-http", host="0.0.0.0", port=8086)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except Exception as e:
        logger.critical(f"Critical error during server startup: {str(e)}", exc_info=True)

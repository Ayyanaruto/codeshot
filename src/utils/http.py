"""HTTP utilities for fetching code from URLs."""

import httpx
from mcp import ErrorData, McpError
from mcp.types import INTERNAL_ERROR
from config.logging_config import get_logger


async def fetch_code_from_url(url: str) -> str:
    """Fetch code content from URLs like GitHub/Gist."""
    logger = get_logger(__name__)
    logger.info(f"Fetching code from URL: {url}")
    
    # Maximum allowed code size (characters) and lines
    MAX_CODE_SIZE = 25000  # Reduced to 25KB for better performance
    MAX_LINES = 300        # Maximum number of lines to prevent huge images
    
    async with httpx.AsyncClient() as client:
        try:
            logger.debug("Sending HTTP request")
            response = await client.get(
                url,
                follow_redirects=True,
                headers={"User-Agent": "Codeshot/1.0"},
                timeout=30,
            )
            
            logger.debug(f"HTTP response: {response.status_code}")
            if response.status_code >= 400:
                logger.error(f"HTTP error: {response.status_code} for URL {url}")
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR, 
                    message=f"Failed to fetch {url} - status code {response.status_code}"
                ))
            
            content_length = len(response.text)
            line_count = response.text.count('\n') + 1
            logger.info(f"Successfully fetched {content_length} characters, {line_count} lines from {url}")
            
            # Check if content is too large (by size or line count)
            needs_truncation = content_length > MAX_CODE_SIZE or line_count > MAX_LINES
            
            if needs_truncation:
                if content_length > MAX_CODE_SIZE:
                    logger.warning(f"Code content is too large ({content_length} chars), truncating to {MAX_CODE_SIZE} chars")
                if line_count > MAX_LINES:
                    logger.warning(f"Code has too many lines ({line_count}), truncating to {MAX_LINES} lines")
                
                # Truncate by lines first (more important for image size)
                lines = response.text.split('\n')
                if len(lines) > MAX_LINES:
                    lines = lines[:MAX_LINES]
                    truncated_content = '\n'.join(lines)
                else:
                    truncated_content = response.text
                
                # Then truncate by character count if still too large
                if len(truncated_content) > MAX_CODE_SIZE:
                    truncated_content = truncated_content[:MAX_CODE_SIZE]
                    # Try to truncate at a line boundary to avoid breaking syntax
                    last_newline = truncated_content.rfind('\n')
                    if last_newline > MAX_CODE_SIZE * 0.8:  # If we're within 20% of the limit
                        truncated_content = truncated_content[:last_newline]
                
                # Add a comment indicating truncation
                final_line_count = truncated_content.count('\n') + 1
                truncated_content += f"\n\n# ... Content truncated for performance"
                truncated_content += f"\n# Original: {content_length} chars, {line_count} lines"
                truncated_content += f"\n# Showing: {len(truncated_content)} chars, {final_line_count} lines"
                
                logger.info(f"Content truncated to {len(truncated_content)} characters, {final_line_count} lines")
                return truncated_content
            
            return response.text
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching {url}: {e!r}")
            raise McpError(ErrorData(
                code=INTERNAL_ERROR, 
                message=f"Failed to fetch {url}: {e!r}"
            ))

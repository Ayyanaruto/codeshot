"""HTTP utilities for fetching code from URLs."""

import httpx
from mcp import ErrorData, McpError
from mcp.types import INTERNAL_ERROR
from config.logging_config import get_logger


async def fetch_code_from_url(url: str) -> str:
    """Fetch code content from URLs like GitHub/Gist."""
    logger = get_logger(__name__)
    logger.info(f"Fetching code from URL: {url}")
    
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
            logger.info(f"Successfully fetched {content_length} characters from {url}")
            return response.text
            
        except httpx.HTTPError as e:
            logger.error(f"HTTP error fetching {url}: {e!r}")
            raise McpError(ErrorData(
                code=INTERNAL_ERROR, 
                message=f"Failed to fetch {url}: {e!r}"
            ))

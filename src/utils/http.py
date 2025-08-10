"""HTTP utilities for fetching code from URLs."""

import httpx
from mcp import ErrorData, McpError
from mcp.types import INTERNAL_ERROR


async def fetch_code_from_url(url: str) -> str:
    """Fetch code content from URLs like GitHub/Gist."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,
                follow_redirects=True,
                headers={"User-Agent": "Codeshot/1.0"},
                timeout=30,
            )
            if response.status_code >= 400:
                raise McpError(ErrorData(
                    code=INTERNAL_ERROR, 
                    message=f"Failed to fetch {url} - status code {response.status_code}"
                ))
            return response.text
        except httpx.HTTPError as e:
            raise McpError(ErrorData(
                code=INTERNAL_ERROR, 
                message=f"Failed to fetch {url}: {e!r}"
            ))

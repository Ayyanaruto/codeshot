"""Test configuration and fixtures."""

import pytest
from src.core.generator import CodeshotGenerator


@pytest.fixture
def sample_code():
    """Sample Python code for testing."""
    return '''
def fibonacci(n):
    """Calculate fibonacci number."""
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
print(fibonacci(10))
'''


@pytest.fixture
def generator():
    """Create a fresh generator instance."""
    return CodeshotGenerator()

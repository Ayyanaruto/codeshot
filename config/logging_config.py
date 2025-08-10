"""Logging configuration for the codeshot application."""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from typing import Optional

from config.constants import (
    LOG_FORMAT, LOG_DATE_FORMAT, DEFAULT_LOG_LEVEL, 
    LOG_FILE_MAX_BYTES, LOG_FILE_BACKUP_COUNT
)


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Format the log record with colors."""
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # Apply color to the level name
        record.levelname = f"{log_color}{record.levelname}{reset_color}"
        
        return super().format(record)


def setup_logging(
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True,
    logger_name: Optional[str] = None
) -> logging.Logger:
    """
    Set up logging configuration for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (defaults to logs/codeshot.log)
        console_output: Whether to output logs to console
        file_output: Whether to output logs to file
        logger_name: Name of the logger (defaults to 'codeshot')
    
    Returns:
        Configured logger instance
    """
    # Get log level from environment or use default
    log_level = level or os.environ.get("LOG_LEVEL", DEFAULT_LOG_LEVEL)
    
    # Get or create logger
    logger_name = logger_name or "codeshot"
    logger = logging.getLogger(logger_name)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Set log level
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create formatters
    console_formatter = ColoredFormatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    file_formatter = logging.Formatter(LOG_FORMAT, datefmt=LOG_DATE_FORMAT)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(console_handler)
    
    # File handler
    if file_output:
        # Create logs directory if it doesn't exist
        if log_file:
            log_path = Path(log_file)
        else:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            log_path = log_dir / "codeshot.log"
        
        # Use rotating file handler to prevent large log files
        file_handler = logging.handlers.RotatingFileHandler(
            log_path,
            maxBytes=LOG_FILE_MAX_BYTES,
            backupCount=LOG_FILE_BACKUP_COUNT,
            encoding='utf-8'
        )
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        name: Name of the module (usually __name__)
    
    Returns:
        Logger instance
    """
    # Ensure the main logger is set up
    if not logging.getLogger("codeshot").handlers:
        setup_logging()
    
    return logging.getLogger(f"codeshot.{name}")


def log_function_call(logger: logging.Logger):
    """
    Decorator to log function calls with parameters and execution time.
    
    Args:
        logger: Logger instance to use
    
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            import time
            
            # Log function entry
            logger.debug(f"Calling {func.__name__} with args={args}, kwargs={kwargs}")
            
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.debug(f"{func.__name__} completed in {execution_time:.3f}s")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"{func.__name__} failed after {execution_time:.3f}s: {str(e)}")
                raise
        
        return wrapper
    return decorator


def log_performance(logger: logging.Logger, operation: str):
    """
    Context manager to log performance of operations.
    
    Args:
        logger: Logger instance to use
        operation: Description of the operation
    
    Usage:
        with log_performance(logger, "image generation"):
            # Your code here
            pass
    """
    class PerformanceLogger:
        def __init__(self, logger, operation):
            self.logger = logger
            self.operation = operation
            self.start_time = None
        
        def __enter__(self):
            self.start_time = __import__('time').time()
            self.logger.debug(f"Starting {self.operation}")
            return self
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            execution_time = __import__('time').time() - self.start_time
            if exc_type:
                self.logger.error(f"{self.operation} failed after {execution_time:.3f}s: {exc_val}")
            else:
                self.logger.info(f"{self.operation} completed in {execution_time:.3f}s")
    
    return PerformanceLogger(logger, operation)

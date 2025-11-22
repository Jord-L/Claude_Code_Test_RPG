"""
Logging Utility
Provides centralized logging for the entire game.
"""

import logging
import os
import sys
from datetime import datetime


class GameLogger:
    """
    Centralized logging system for the game.
    Logs to both console and file with different levels.
    """
    
    def __init__(self, name="OnePieceRPG", log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
        """
        Initialize the game logger.
        
        Args:
            name: Logger name
            log_dir: Directory to store log files
            console_level: Logging level for console output
            file_level: Logging level for file output
        """
        self.name = name
        self.log_dir = log_dir
        
        # Create logs directory if it doesn't exist
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)  # Capture everything, handlers will filter
        
        # Remove existing handlers to avoid duplicates
        self.logger.handlers.clear()
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)-8s] [%(name)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        console_formatter = logging.Formatter(
            '[%(levelname)-8s] %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(console_level)
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler (session log)
        session_log_file = os.path.join(
            log_dir,
            f"game_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        file_handler = logging.FileHandler(session_log_file, encoding='utf-8')
        file_handler.setLevel(file_level)
        file_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(file_handler)
        
        # Also create/append to a general log file
        general_log_file = os.path.join(log_dir, "game_general.log")
        general_handler = logging.FileHandler(general_log_file, encoding='utf-8')
        general_handler.setLevel(logging.INFO)
        general_handler.setFormatter(detailed_formatter)
        self.logger.addHandler(general_handler)
        
        self.session_log_file = session_log_file
        self.general_log_file = general_log_file
    
    def debug(self, message):
        """Log debug message."""
        self.logger.debug(message)
    
    def info(self, message):
        """Log info message."""
        self.logger.info(message)
    
    def warning(self, message):
        """Log warning message."""
        self.logger.warning(message)
    
    def error(self, message):
        """Log error message."""
        self.logger.error(message)
    
    def critical(self, message):
        """Log critical message."""
        self.logger.critical(message)
    
    def exception(self, message):
        """Log exception with traceback."""
        self.logger.exception(message)
    
    def separator(self, char="=", length=70):
        """Log a separator line."""
        self.logger.info(char * length)
    
    def section(self, title):
        """Log a section header."""
        self.separator()
        self.logger.info(f" {title}")
        self.separator()
    
    def get_session_log_path(self):
        """Get the path to the current session log file."""
        return self.session_log_file
    
    def get_general_log_path(self):
        """Get the path to the general log file."""
        return self.general_log_file


# Global logger instance
_global_logger = None


def init_logger(name="OnePieceRPG", log_dir="logs", console_level=logging.INFO, file_level=logging.DEBUG):
    """
    Initialize the global logger.
    
    Args:
        name: Logger name
        log_dir: Directory to store log files
        console_level: Logging level for console output
        file_level: Logging level for file output
    
    Returns:
        GameLogger instance
    """
    global _global_logger
    _global_logger = GameLogger(name, log_dir, console_level, file_level)
    return _global_logger


def get_logger():
    """
    Get the global logger instance.
    
    Returns:
        GameLogger instance
    
    Raises:
        RuntimeError: If logger hasn't been initialized
    """
    global _global_logger
    if _global_logger is None:
        # Auto-initialize with defaults if not initialized
        init_logger()
    return _global_logger


# Convenience functions for quick logging
def debug(message):
    """Log debug message."""
    get_logger().debug(message)


def info(message):
    """Log info message."""
    get_logger().info(message)


def warning(message):
    """Log warning message."""
    get_logger().warning(message)


def error(message):
    """Log error message."""
    get_logger().error(message)


def critical(message):
    """Log critical message."""
    get_logger().critical(message)


def exception(message):
    """Log exception with traceback."""
    get_logger().exception(message)


def separator(char="=", length=70):
    """Log a separator line."""
    get_logger().separator(char, length)


def section(title):
    """Log a section header."""
    get_logger().section(title)

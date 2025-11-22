"""
Shared logging setup for all test files.
"""
import logging
import sys
import os
from datetime import datetime
import time

def setup_test_logger(test_name):
    """
    Setup logger for test files.
    
    Args:
        test_name: Name of the test (e.g., 'test_phase1_part3')
    
    Returns:
        Configured logger instance
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers = []
    
    # File handler with detailed formatting
    log_file = os.path.join(log_dir, f"{test_name}.log")
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Console handler (cleaner format for user viewing)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    return logger

def log_test_start(logger, test_name):
    """Log test start with system info."""
    logger.info("=" * 60)
    logger.info(test_name)
    logger.info("=" * 60)
    logger.info("")
    logger.debug(f"Test started at: {datetime.now()}")
    logger.debug(f"Python version: {sys.version}")
    logger.debug(f"Working directory: {os.getcwd()}")

def log_test_end(logger, log_filename):
    """Log test completion."""
    logger.debug(f"Test completed at: {datetime.now()}")
    logger.debug(f"Log file saved to: logs/{log_filename}")

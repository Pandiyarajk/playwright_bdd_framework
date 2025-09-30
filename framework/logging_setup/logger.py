"""Logging configuration and setup."""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
import colorlog


def setup_logger(config_manager=None):
    """
    Setup and configure logger.
    
    Args:
        config_manager: Configuration manager instance
        
    Returns:
        Logger instance
    """
    if config_manager:
        log_level = config_manager.get('logging', 'level', 'INFO')
        log_to_file = config_manager.get('logging', 'log_to_file', True)
        log_to_console = config_manager.get('logging', 'log_to_console', True)
        log_file_path = config_manager.get('logging', 'log_file_path', 'logs/automation.log')
        log_format = config_manager.get('logging', 'log_format', 
                                       '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    else:
        log_level = 'INFO'
        log_to_file = True
        log_to_console = True
        log_file_path = 'logs/automation.log'
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Create logger
    logger = logging.getLogger('AutomationFramework')
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Console handler with color
    if log_to_console:
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, log_level.upper()))
        
        console_format = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        # Create log directory
        log_path = Path(log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add timestamp to log file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file_with_timestamp = log_path.parent / f"{log_path.stem}_{timestamp}{log_path.suffix}"
        
        file_handler = RotatingFileHandler(
            log_file_with_timestamp,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        file_format = logging.Formatter(
            log_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)
        
        # Also create a latest.log symlink
        latest_log = log_path.parent / 'latest.log'
        try:
            if latest_log.exists():
                latest_log.unlink()
            # Create regular copy instead of symlink for cross-platform compatibility
            import shutil
            shutil.copy2(log_file_with_timestamp, latest_log)
        except:
            pass
    
    return logger
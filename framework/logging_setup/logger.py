"""Logging configuration and setup using powerlogger."""

from powerlogger import get_logger


def setup_logger(config_manager=None, name="AutomationFramework"):
    """
    Setup and configure logger using powerlogger.
    
    Args:
        config_manager: Configuration manager instance (optional, for backward compatibility)
        name: Logger name
        
    Returns:
        Powerlogger instance
    """
    # Get logger from powerlogger
    # powerlogger automatically handles colored console output, file logging,
    # and provides emoji support out of the box
    logger = get_logger(name)
    
    return logger
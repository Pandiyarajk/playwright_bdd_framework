"""
Playwright Python BDD Test Automation Framework

A comprehensive test automation framework with BDD support, multiple data sources,
OCR/image recognition, and enterprise integrations.
"""

__version__ = "1.0.0"
__author__ = "Automation Team"

from framework.config.config_manager import ConfigManager
from framework.playwright_wrapper.playwright_actions import PlaywrightActions
from framework.utils.date_utils import DateUtils
from framework.utils.ocr_utils import OCRUtils
from framework.utils.image_utils import ImageUtils

__all__ = [
    "ConfigManager",
    "PlaywrightActions",
    "DateUtils",
    "OCRUtils",
    "ImageUtils",
]
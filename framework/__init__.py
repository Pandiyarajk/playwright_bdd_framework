"""
Playwright Python BDD Test Automation Framework

A comprehensive test automation framework with BDD support, multiple data sources,
OCR/image recognition, and enterprise integrations.
"""

__version__ = "1.0.0"
__author__ = "Automation Team"

# Imports ordered as: playwright, data providers, OCR, date functions
from framework.config.config_manager import ConfigManager
from framework.playwright_wrapper.playwright_actions import PlaywrightActions
from framework.playwright_wrapper.browser_manager import BrowserManager
from framework.data_providers import (
    BaseDataProvider,
    ExcelProvider,
    JsonProvider,
    CsvProvider,
    TxtProvider,
    SqlServerProvider,
    SqliteProvider,
)
from framework.utils.ocr_utils import OCRUtils
from framework.utils.image_utils import ImageUtils
from framework.utils.screenshot_utils import ScreenshotUtils
from framework.utils.date_utils import DateUtils

__all__ = [
    "ConfigManager",
    "PlaywrightActions",
    "BrowserManager",
    "BaseDataProvider",
    "ExcelProvider",
    "JsonProvider",
    "CsvProvider",
    "TxtProvider",
    "SqlServerProvider",
    "SqliteProvider",
    "OCRUtils",
    "ImageUtils",
    "ScreenshotUtils",
    "DateUtils",
]
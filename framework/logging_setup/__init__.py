"""Logging setup module."""

from framework.logging_setup.logger import setup_logger
from framework.logging_setup.system_monitor import SystemMonitor

__all__ = ["setup_logger", "SystemMonitor"]
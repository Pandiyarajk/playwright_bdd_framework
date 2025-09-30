"""Screenshot utility functions that work on any screen state, including locked Windows screens."""

from pathlib import Path
from typing import Optional, Tuple
import mss
from PIL import Image


class ScreenshotUtils:
    """OS-level screenshot utilities that work even on locked Windows screens."""
    
    @staticmethod
    def take_screenshot(
        path: Optional[str] = None,
        monitor: int = 0,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> str:
        """
        Take OS-level screenshot that works on locked Windows screens.
        
        This method uses MSS (Multiple Screen Shot) library which works at the
        OS level and can capture screenshots even when the screen is locked.
        
        Args:
            path: Path to save screenshot (auto-generated if not provided)
            monitor: Monitor number (0 = all monitors, 1 = primary, 2 = secondary, etc.)
            region: Optional region to capture (left, top, width, height)
            
        Returns:
            Path to saved screenshot
        """
        # Auto-generate path if not provided
        if not path:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            path = f'screenshots/screenshot_{timestamp}.png'
        
        # Ensure directory exists
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        with mss.mss() as sct:
            if region:
                # Capture specific region
                monitor_config = {
                    "left": region[0],
                    "top": region[1],
                    "width": region[2],
                    "height": region[3]
                }
                screenshot = sct.grab(monitor_config)
            else:
                # Capture specified monitor
                if monitor == 0:
                    # Capture all monitors
                    screenshot = sct.grab(sct.monitors[0])
                else:
                    # Capture specific monitor
                    screenshot = sct.grab(sct.monitors[monitor])
            
            # Convert to PIL Image and save
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            img.save(path)
        
        return path
    
    @staticmethod
    def get_monitor_info() -> list:
        """
        Get information about all available monitors.
        
        Returns:
            List of monitor dictionaries with position and size information
        """
        with mss.mss() as sct:
            return sct.monitors
    
    @staticmethod
    def take_multi_monitor_screenshot(path: Optional[str] = None) -> str:
        """
        Take screenshot of all monitors combined.
        
        Args:
            path: Path to save screenshot (auto-generated if not provided)
            
        Returns:
            Path to saved screenshot
        """
        return ScreenshotUtils.take_screenshot(path=path, monitor=0)
    
    @staticmethod
    def take_primary_monitor_screenshot(path: Optional[str] = None) -> str:
        """
        Take screenshot of primary monitor only.
        
        Args:
            path: Path to save screenshot (auto-generated if not provided)
            
        Returns:
            Path to saved screenshot
        """
        return ScreenshotUtils.take_screenshot(path=path, monitor=1)
    
    @staticmethod
    def take_region_screenshot(
        left: int,
        top: int,
        width: int,
        height: int,
        path: Optional[str] = None
    ) -> str:
        """
        Take screenshot of specific screen region.
        
        Args:
            left: Left coordinate
            top: Top coordinate
            width: Width of region
            height: Height of region
            path: Path to save screenshot (auto-generated if not provided)
            
        Returns:
            Path to saved screenshot
        """
        return ScreenshotUtils.take_screenshot(
            path=path,
            region=(left, top, width, height)
        )

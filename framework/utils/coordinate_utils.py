"""Coordinate and position utilities for element interactions."""

from typing import Dict, Optional, Tuple
from playwright.sync_api import Page, Locator


class CoordinateUtils:
    """Utilities for coordinate-based interactions."""
    
    @staticmethod
    def get_element_coordinates(locator: Locator) -> Dict[str, float]:
        """
        Get center coordinates of an element.
        
        Args:
            locator: Playwright locator
            
        Returns:
            Dictionary with x, y coordinates and bounding box
        """
        box = locator.bounding_box()
        
        if not box:
            raise ValueError("Element not visible or does not exist")
        
        center_x = box['x'] + box['width'] / 2
        center_y = box['y'] + box['height'] / 2
        
        return {
            'x': center_x,
            'y': center_y,
            'left': box['x'],
            'top': box['y'],
            'right': box['x'] + box['width'],
            'bottom': box['y'] + box['height'],
            'width': box['width'],
            'height': box['height']
        }
    
    @staticmethod
    def click_at_coordinates(
        page: Page,
        x: float,
        y: float,
        button: str = 'left',
        click_count: int = 1,
        delay: Optional[int] = None
    ) -> None:
        """
        Click at specific coordinates.
        
        Args:
            page: Playwright page
            x: X coordinate
            y: Y coordinate
            button: Mouse button ('left', 'right', 'middle')
            click_count: Number of clicks (1 for single, 2 for double)
            delay: Delay between mousedown and mouseup in ms
        """
        page.mouse.click(x, y, button=button, click_count=click_count, delay=delay)
    
    @staticmethod
    def click_element_at_offset(
        locator: Locator,
        offset_x: float = 0,
        offset_y: float = 0,
        button: str = 'left'
    ) -> None:
        """
        Click element with offset from center.
        
        Args:
            locator: Playwright locator
            offset_x: X offset from center
            offset_y: Y offset from center
            button: Mouse button
        """
        coords = CoordinateUtils.get_element_coordinates(locator)
        x = coords['x'] + offset_x
        y = coords['y'] + offset_y
        
        page = locator.page
        page.mouse.click(x, y, button=button)
    
    @staticmethod
    def hover_at_coordinates(page: Page, x: float, y: float) -> None:
        """
        Hover at specific coordinates.
        
        Args:
            page: Playwright page
            x: X coordinate
            y: Y coordinate
        """
        page.mouse.move(x, y)
    
    @staticmethod
    def drag_and_drop_coordinates(
        page: Page,
        from_x: float,
        from_y: float,
        to_x: float,
        to_y: float,
        steps: int = 10
    ) -> None:
        """
        Drag from one coordinate to another.
        
        Args:
            page: Playwright page
            from_x: Starting X coordinate
            from_y: Starting Y coordinate
            to_x: Ending X coordinate
            to_y: Ending Y coordinate
            steps: Number of intermediate steps
        """
        page.mouse.move(from_x, from_y)
        page.mouse.down()
        page.mouse.move(to_x, to_y, steps=steps)
        page.mouse.up()
    
    @staticmethod
    def drag_element_to_coordinates(
        locator: Locator,
        to_x: float,
        to_y: float,
        steps: int = 10
    ) -> None:
        """
        Drag element to specific coordinates.
        
        Args:
            locator: Source element locator
            to_x: Target X coordinate
            to_y: Target Y coordinate
            steps: Number of intermediate steps
        """
        coords = CoordinateUtils.get_element_coordinates(locator)
        page = locator.page
        
        CoordinateUtils.drag_and_drop_coordinates(
            page,
            coords['x'],
            coords['y'],
            to_x,
            to_y,
            steps
        )
    
    @staticmethod
    def drag_element_to_element(
        source_locator: Locator,
        target_locator: Locator,
        steps: int = 10
    ) -> None:
        """
        Drag one element to another element.
        
        Args:
            source_locator: Source element locator
            target_locator: Target element locator
            steps: Number of intermediate steps
        """
        source_coords = CoordinateUtils.get_element_coordinates(source_locator)
        target_coords = CoordinateUtils.get_element_coordinates(target_locator)
        
        page = source_locator.page
        
        CoordinateUtils.drag_and_drop_coordinates(
            page,
            source_coords['x'],
            source_coords['y'],
            target_coords['x'],
            target_coords['y'],
            steps
        )
    
    @staticmethod
    def get_viewport_coordinates(page: Page) -> Dict[str, int]:
        """
        Get viewport dimensions.
        
        Args:
            page: Playwright page
            
        Returns:
            Dictionary with width and height
        """
        viewport = page.viewport_size
        return {
            'width': viewport['width'],
            'height': viewport['height']
        }
    
    @staticmethod
    def is_element_in_viewport(locator: Locator) -> bool:
        """
        Check if element is within viewport.
        
        Args:
            locator: Playwright locator
            
        Returns:
            True if element is in viewport
        """
        coords = CoordinateUtils.get_element_coordinates(locator)
        viewport = CoordinateUtils.get_viewport_coordinates(locator.page)
        
        return (
            coords['left'] >= 0 and
            coords['top'] >= 0 and
            coords['right'] <= viewport['width'] and
            coords['bottom'] <= viewport['height']
        )
    
    @staticmethod
    def scroll_to_coordinates(
        page: Page,
        x: float = 0,
        y: float = 0
    ) -> None:
        """
        Scroll page to specific coordinates.
        
        Args:
            page: Playwright page
            x: X scroll position
            y: Y scroll position
        """
        page.evaluate(f"window.scrollTo({x}, {y})")
    
    @staticmethod
    def get_scroll_position(page: Page) -> Dict[str, float]:
        """
        Get current scroll position.
        
        Args:
            page: Playwright page
            
        Returns:
            Dictionary with x and y scroll position
        """
        scroll_x = page.evaluate("window.pageXOffset")
        scroll_y = page.evaluate("window.pageYOffset")
        
        return {'x': scroll_x, 'y': scroll_y}
    
    @staticmethod
    def calculate_distance(
        x1: float,
        y1: float,
        x2: float,
        y2: float
    ) -> float:
        """
        Calculate distance between two points.
        
        Args:
            x1: First point X coordinate
            y1: First point Y coordinate
            x2: Second point X coordinate
            y2: Second point Y coordinate
            
        Returns:
            Distance in pixels
        """
        import math
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    @staticmethod
    def get_element_relative_position(
        element_locator: Locator,
        reference_locator: Locator
    ) -> Dict[str, float]:
        """
        Get element position relative to another element.
        
        Args:
            element_locator: Element to check
            reference_locator: Reference element
            
        Returns:
            Dictionary with relative positions
        """
        element_coords = CoordinateUtils.get_element_coordinates(element_locator)
        reference_coords = CoordinateUtils.get_element_coordinates(reference_locator)
        
        return {
            'offset_x': element_coords['x'] - reference_coords['x'],
            'offset_y': element_coords['y'] - reference_coords['y'],
            'is_above': element_coords['bottom'] < reference_coords['top'],
            'is_below': element_coords['top'] > reference_coords['bottom'],
            'is_left': element_coords['right'] < reference_coords['left'],
            'is_right': element_coords['left'] > reference_coords['right']
        }
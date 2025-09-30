"""Comprehensive Playwright action wrappers."""

import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from playwright.sync_api import Page, Locator, expect
from framework.utils.coordinate_utils import CoordinateUtils


class PlaywrightActions:
    """Reusable Playwright action functions."""
    
    def __init__(self, page: Page):
        """
        Initialize Playwright actions.
        
        Args:
            page: Playwright page object
        """
        self.page = page
        self.coordinate_utils = CoordinateUtils()
    
    # Navigation methods
    
    def navigate(self, url: str, wait_until: str = 'networkidle') -> None:
        """
        Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_until: Wait until state ('load', 'domcontentloaded', 'networkidle')
        """
        self.page.goto(url, wait_until=wait_until)
    
    def reload(self, wait_until: str = 'networkidle') -> None:
        """
        Reload current page.
        
        Args:
            wait_until: Wait until state
        """
        self.page.reload(wait_until=wait_until)
    
    def go_back(self, wait_until: str = 'networkidle') -> None:
        """Navigate back."""
        self.page.go_back(wait_until=wait_until)
    
    def go_forward(self, wait_until: str = 'networkidle') -> None:
        """Navigate forward."""
        self.page.go_forward(wait_until=wait_until)
    
    def get_current_url(self) -> str:
        """Get current page URL."""
        return self.page.url
    
    def get_title(self) -> str:
        """Get page title."""
        return self.page.title()
    
    # Element interaction methods
    
    def click(
        self,
        selector: str,
        timeout: Optional[int] = None,
        force: bool = False,
        button: str = 'left',
        click_count: int = 1
    ) -> None:
        """
        Click element.
        
        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
            force: Force click even if element is not actionable
            button: Mouse button ('left', 'right', 'middle')
            click_count: Number of clicks
        """
        locator = self.page.locator(selector)
        locator.click(
            timeout=timeout,
            force=force,
            button=button,
            click_count=click_count
        )
    
    def double_click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Double-click element."""
        self.click(selector, timeout=timeout, click_count=2)
    
    def right_click(self, selector: str, timeout: Optional[int] = None) -> None:
        """Right-click element."""
        self.click(selector, timeout=timeout, button='right')
    
    def click_by_coordinates(
        self,
        x: float,
        y: float,
        button: str = 'left',
        click_count: int = 1
    ) -> None:
        """
        Click at coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button
            click_count: Number of clicks
        """
        self.coordinate_utils.click_at_coordinates(
            self.page, x, y, button, click_count
        )
    
    def type_text(
        self,
        selector: str,
        text: str,
        delay: Optional[int] = None,
        clear_first: bool = True
    ) -> None:
        """
        Type text into element.
        
        Args:
            selector: Element selector
            text: Text to type
            delay: Delay between key presses in ms
            clear_first: Clear existing text first
        """
        locator = self.page.locator(selector)
        
        if clear_first:
            locator.clear()
        
        if delay:
            locator.type(text, delay=delay)
        else:
            locator.fill(text)
    
    def fill(self, selector: str, text: str) -> None:
        """
        Fill input field.
        
        Args:
            selector: Element selector
            text: Text to fill
        """
        self.page.locator(selector).fill(text)
    
    def clear(self, selector: str) -> None:
        """Clear input field."""
        self.page.locator(selector).clear()
    
    def press_key(self, selector: str, key: str) -> None:
        """
        Press keyboard key.
        
        Args:
            selector: Element selector
            key: Key to press (e.g., 'Enter', 'Tab', 'Escape')
        """
        self.page.locator(selector).press(key)
    
    def check(self, selector: str, timeout: Optional[int] = None) -> None:
        """Check checkbox or radio button."""
        self.page.locator(selector).check(timeout=timeout)
    
    def uncheck(self, selector: str, timeout: Optional[int] = None) -> None:
        """Uncheck checkbox."""
        self.page.locator(selector).uncheck(timeout=timeout)
    
    def select_option(
        self,
        selector: str,
        value: Optional[Union[str, List[str]]] = None,
        label: Optional[Union[str, List[str]]] = None,
        index: Optional[Union[int, List[int]]] = None
    ) -> None:
        """
        Select dropdown option.
        
        Args:
            selector: Element selector
            value: Option value(s)
            label: Option label(s)
            index: Option index(es)
        """
        locator = self.page.locator(selector)
        
        if value:
            locator.select_option(value=value)
        elif label:
            locator.select_option(label=label)
        elif index is not None:
            locator.select_option(index=index)
    
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """Hover over element."""
        self.page.locator(selector).hover(timeout=timeout)
    
    def drag_and_drop(
        self,
        source_selector: str,
        target_selector: str,
        timeout: Optional[int] = None
    ) -> None:
        """
        Drag and drop element.
        
        Args:
            source_selector: Source element selector
            target_selector: Target element selector
            timeout: Timeout in milliseconds
        """
        self.page.locator(source_selector).drag_to(
            self.page.locator(target_selector),
            timeout=timeout
        )
    
    def upload_file(self, selector: str, file_path: Union[str, List[str]]) -> None:
        """
        Upload file(s).
        
        Args:
            selector: File input selector
            file_path: Path to file or list of paths
        """
        self.page.locator(selector).set_input_files(file_path)
    
    def focus(self, selector: str) -> None:
        """Focus on element."""
        self.page.locator(selector).focus()
    
    # Wait methods
    
    def wait_for_selector(
        self,
        selector: str,
        state: str = 'visible',
        timeout: Optional[int] = None
    ) -> None:
        """
        Wait for element.
        
        Args:
            selector: Element selector
            state: State to wait for ('attached', 'detached', 'visible', 'hidden')
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_selector(selector, state=state, timeout=timeout)
    
    def wait_for_url(
        self,
        url: Union[str, callable],
        timeout: Optional[int] = None
    ) -> None:
        """
        Wait for URL.
        
        Args:
            url: URL string or predicate function
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_url(url, timeout=timeout)
    
    def wait_for_load_state(self, state: str = 'networkidle') -> None:
        """
        Wait for load state.
        
        Args:
            state: Load state ('load', 'domcontentloaded', 'networkidle')
        """
        self.page.wait_for_load_state(state)
    
    def wait_for_timeout(self, timeout: int) -> None:
        """
        Wait for specified time.
        
        Args:
            timeout: Time to wait in milliseconds
        """
        self.page.wait_for_timeout(timeout)
    
    def wait_and_click(
        self,
        selector: str,
        timeout: Optional[int] = None,
        wait_state: str = 'visible'
    ) -> None:
        """
        Wait for element and click.
        
        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
            wait_state: State to wait for
        """
        self.wait_for_selector(selector, state=wait_state, timeout=timeout)
        self.click(selector, timeout=timeout)
    
    # Get methods
    
    def get_text(self, selector: str) -> str:
        """Get element text content."""
        return self.page.locator(selector).text_content() or ""
    
    def get_inner_text(self, selector: str) -> str:
        """Get element inner text."""
        return self.page.locator(selector).inner_text()
    
    def get_inner_html(self, selector: str) -> str:
        """Get element inner HTML."""
        return self.page.locator(selector).inner_html()
    
    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """Get element attribute value."""
        return self.page.locator(selector).get_attribute(attribute)
    
    def get_value(self, selector: str) -> str:
        """Get input value."""
        return self.page.locator(selector).input_value()
    
    def is_visible(self, selector: str, timeout: int = 1000) -> bool:
        """Check if element is visible."""
        try:
            return self.page.locator(selector).is_visible(timeout=timeout)
        except:
            return False
    
    def is_hidden(self, selector: str) -> bool:
        """Check if element is hidden."""
        return self.page.locator(selector).is_hidden()
    
    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled."""
        return self.page.locator(selector).is_enabled()
    
    def is_disabled(self, selector: str) -> bool:
        """Check if element is disabled."""
        return self.page.locator(selector).is_disabled()
    
    def is_checked(self, selector: str) -> bool:
        """Check if checkbox/radio is checked."""
        return self.page.locator(selector).is_checked()
    
    def count(self, selector: str) -> int:
        """Get count of matching elements."""
        return self.page.locator(selector).count()
    
    # Assertion methods
    
    def assert_visible(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is visible."""
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)
    
    def assert_hidden(self, selector: str, timeout: Optional[int] = None) -> None:
        """Assert element is hidden."""
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)
    
    def assert_text(
        self,
        selector: str,
        expected_text: str,
        timeout: Optional[int] = None
    ) -> None:
        """Assert element has text."""
        expect(self.page.locator(selector)).to_have_text(expected_text, timeout=timeout)
    
    def assert_contains_text(
        self,
        selector: str,
        expected_text: str,
        timeout: Optional[int] = None
    ) -> None:
        """Assert element contains text."""
        expect(self.page.locator(selector)).to_contain_text(expected_text, timeout=timeout)
    
    def assert_value(
        self,
        selector: str,
        expected_value: str,
        timeout: Optional[int] = None
    ) -> None:
        """Assert input has value."""
        expect(self.page.locator(selector)).to_have_value(expected_value, timeout=timeout)
    
    def assert_url(self, expected_url: Union[str, callable], timeout: Optional[int] = None) -> None:
        """Assert page URL."""
        expect(self.page).to_have_url(expected_url, timeout=timeout)
    
    def assert_title(self, expected_title: Union[str, callable], timeout: Optional[int] = None) -> None:
        """Assert page title."""
        expect(self.page).to_have_title(expected_title, timeout=timeout)
    
    # Screenshot and video
    
    def take_screenshot(
        self,
        path: Optional[str] = None,
        full_page: bool = False
    ) -> bytes:
        """
        Take screenshot.
        
        Args:
            path: Path to save screenshot
            full_page: Capture full page
            
        Returns:
            Screenshot bytes
        """
        if path:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        
        return self.page.screenshot(path=path, full_page=full_page)
    
    def take_element_screenshot(self, selector: str, path: str) -> bytes:
        """Take screenshot of specific element."""
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        return self.page.locator(selector).screenshot(path=path)
    
    # JavaScript execution
    
    def execute_script(self, script: str, *args) -> Any:
        """Execute JavaScript."""
        return self.page.evaluate(script, *args)
    
    def execute_script_on_element(
        self,
        selector: str,
        script: str,
        *args
    ) -> Any:
        """Execute JavaScript on element."""
        return self.page.locator(selector).evaluate(script, *args)
    
    # Frame methods
    
    def switch_to_frame(self, selector: str) -> Any:
        """Switch to iframe."""
        return self.page.frame_locator(selector)
    
    # Alert/Dialog methods
    
    def handle_dialog(
        self,
        action: str = 'accept',
        prompt_text: Optional[str] = None
    ) -> None:
        """
        Handle JavaScript dialog.
        
        Args:
            action: Action to perform ('accept' or 'dismiss')
            prompt_text: Text to enter in prompt
        """
        def dialog_handler(dialog):
            if prompt_text and dialog.type == 'prompt':
                dialog.accept(prompt_text)
            elif action == 'accept':
                dialog.accept()
            else:
                dialog.dismiss()
        
        self.page.on('dialog', dialog_handler)
    
    # Scroll methods
    
    def scroll_to_element(self, selector: str) -> None:
        """Scroll element into view."""
        self.page.locator(selector).scroll_into_view_if_needed()
    
    def scroll_to_bottom(self) -> None:
        """Scroll to bottom of page."""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    
    def scroll_to_top(self) -> None:
        """Scroll to top of page."""
        self.page.evaluate("window.scrollTo(0, 0)")
    
    # Cookie methods
    
    def get_cookies(self) -> List[Dict]:
        """Get all cookies."""
        return self.page.context.cookies()
    
    def add_cookie(self, cookie: Dict) -> None:
        """Add cookie."""
        self.page.context.add_cookies([cookie])
    
    def clear_cookies(self) -> None:
        """Clear all cookies."""
        self.page.context.clear_cookies()
    
    # Local/Session Storage
    
    def set_local_storage(self, key: str, value: str) -> None:
        """Set local storage item."""
        self.page.evaluate(f"localStorage.setItem('{key}', '{value}')")
    
    def get_local_storage(self, key: str) -> Optional[str]:
        """Get local storage item."""
        return self.page.evaluate(f"localStorage.getItem('{key}')")
    
    def clear_local_storage(self) -> None:
        """Clear local storage."""
        self.page.evaluate("localStorage.clear()")
    
    # Network methods
    
    def wait_for_response(
        self,
        url_pattern: Union[str, callable],
        timeout: Optional[int] = None
    ) -> Any:
        """Wait for HTTP response."""
        return self.page.wait_for_response(url_pattern, timeout=timeout)
    
    def wait_for_request(
        self,
        url_pattern: Union[str, callable],
        timeout: Optional[int] = None
    ) -> Any:
        """Wait for HTTP request."""
        return self.page.wait_for_request(url_pattern, timeout=timeout)
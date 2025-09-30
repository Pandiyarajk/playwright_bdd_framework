"""Browser management for Playwright."""

from typing import Dict, Optional
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Playwright
from framework.config.config_manager import ConfigManager


class BrowserManager:
    """Manages Playwright browser lifecycle."""
    
    def __init__(self, config: Optional[ConfigManager] = None):
        """
        Initialize browser manager.
        
        Args:
            config: Configuration manager instance
        """
        self.config = config or ConfigManager()
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    def start_browser(
        self,
        browser_type: Optional[str] = None,
        headless: Optional[bool] = None,
        **kwargs
    ) -> Page:
        """
        Start browser and return page.
        
        Args:
            browser_type: Browser type ('chromium', 'firefox', 'webkit')
            headless: Run in headless mode
            **kwargs: Additional browser launch arguments
            
        Returns:
            Playwright Page object
        """
        # Get configuration
        browser_type = browser_type or self.config.get('framework', 'browser', 'chromium')
        headless = headless if headless is not None else self.config.get('framework', 'headless', False)
        slow_mo = self.config.get('framework', 'slow_mo', 0)
        
        # Start Playwright
        self.playwright = sync_playwright().start()
        
        # Launch browser
        browser_launcher = getattr(self.playwright, browser_type)
        
        launch_args = {
            'headless': headless,
            'slow_mo': slow_mo,
            **kwargs
        }
        
        self.browser = browser_launcher.launch(**launch_args)
        
        # Create context
        context_options = self._get_context_options()
        self.context = self.browser.new_context(**context_options)
        
        # Create page
        self.page = self.context.new_page()
        
        # Set default timeout
        timeout = self.config.get('framework', 'timeout', 30000)
        self.page.set_default_timeout(timeout)
        
        return self.page
    
    def _get_context_options(self) -> Dict:
        """Get browser context options from configuration."""
        options = {}
        
        # Viewport
        viewport_width = self.config.get('framework', 'viewport_width', 1920)
        viewport_height = self.config.get('framework', 'viewport_height', 1080)
        options['viewport'] = {
            'width': viewport_width,
            'height': viewport_height
        }
        
        # Playwright section options
        if self.config.get('playwright', 'accept_downloads'):
            options['accept_downloads'] = True
        
        if self.config.get('playwright', 'ignore_https_errors'):
            options['ignore_https_errors'] = True
        
        locale = self.config.get('playwright', 'locale')
        if locale:
            options['locale'] = locale
        
        timezone_id = self.config.get('playwright', 'timezone_id')
        if timezone_id:
            options['timezone_id'] = timezone_id
        
        if self.config.get('playwright', 'has_touch'):
            options['has_touch'] = True
        
        if self.config.get('playwright', 'is_mobile'):
            options['is_mobile'] = True
        
        # Tracing
        if self.config.get('framework', 'trace_on_failure'):
            options['record_trace_dir'] = 'traces'
        
        return options
    
    def new_page(self) -> Page:
        """
        Create a new page in current context.
        
        Returns:
            New Playwright Page object
        """
        if not self.context:
            raise RuntimeError("Browser context not initialized")
        
        page = self.context.new_page()
        timeout = self.config.get('framework', 'timeout', 30000)
        page.set_default_timeout(timeout)
        
        return page
    
    def close_page(self, page: Optional[Page] = None) -> None:
        """
        Close a page.
        
        Args:
            page: Page to close (default: current page)
        """
        target_page = page or self.page
        if target_page:
            target_page.close()
            if target_page == self.page:
                self.page = None
    
    def close_context(self) -> None:
        """Close browser context."""
        if self.context:
            self.context.close()
            self.context = None
            self.page = None
    
    def close_browser(self) -> None:
        """Close browser."""
        if self.browser:
            self.browser.close()
            self.browser = None
            self.context = None
            self.page = None
    
    def stop(self) -> None:
        """Stop Playwright and clean up all resources."""
        if self.page:
            self.page.close()
        
        if self.context:
            self.context.close()
        
        if self.browser:
            self.browser.close()
        
        if self.playwright:
            self.playwright.stop()
        
        self.page = None
        self.context = None
        self.browser = None
        self.playwright = None
    
    def __enter__(self):
        """Context manager entry."""
        self.start_browser()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
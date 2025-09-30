"""
Example usage of screenshot utilities with locked Windows screen support.

This module demonstrates various ways to take screenshots using the framework,
including OS-level screenshots that work on locked Windows screens.
"""

from framework.utils import ScreenshotUtils
from framework.playwright_wrapper import PlaywrightActions


def example_os_level_screenshots():
    """Examples of OS-level screenshots that work on locked screens."""
    
    print("=== OS-Level Screenshot Examples ===\n")
    
    # Example 1: Take screenshot of all monitors
    print("1. Taking screenshot of all monitors...")
    path = ScreenshotUtils.take_screenshot("screenshots/all_monitors.png")
    print(f"   Saved to: {path}\n")
    
    # Example 2: Take screenshot of primary monitor only
    print("2. Taking screenshot of primary monitor...")
    path = ScreenshotUtils.take_primary_monitor_screenshot("screenshots/primary.png")
    print(f"   Saved to: {path}\n")
    
    # Example 3: Get monitor information
    print("3. Getting monitor information...")
    monitors = ScreenshotUtils.get_monitor_info()
    for i, monitor in enumerate(monitors):
        print(f"   Monitor {i}: {monitor}")
    print()
    
    # Example 4: Take screenshot of specific region
    print("4. Taking screenshot of specific region (top-left 800x600)...")
    path = ScreenshotUtils.take_region_screenshot(
        left=0, top=0, width=800, height=600,
        path="screenshots/region.png"
    )
    print(f"   Saved to: {path}\n")
    
    # Example 5: Auto-generated filename
    print("5. Taking screenshot with auto-generated filename...")
    path = ScreenshotUtils.take_screenshot()
    print(f"   Saved to: {path}\n")


def example_playwright_screenshots(page):
    """Examples of Playwright screenshots with optional page parameter."""
    
    print("=== Playwright Screenshot Examples ===\n")
    
    # Initialize actions
    actions = PlaywrightActions(page)
    
    # Example 1: Regular Playwright screenshot
    print("1. Taking regular Playwright screenshot...")
    actions.take_screenshot("screenshots/playwright_page.png", full_page=True)
    print("   Screenshot taken\n")
    
    # Example 2: Screenshot with different page object
    print("2. Taking screenshot with optional page parameter...")
    # If you have another page object
    # actions.take_screenshot("screenshots/other_page.png", page=other_page)
    print("   (Would use: actions.take_screenshot(path, page=other_page))\n")
    
    # Example 3: Using OS-level screenshot from PlaywrightActions
    print("3. Taking OS-level screenshot from PlaywrightActions...")
    actions.take_screenshot("screenshots/os_level.png", use_os_screenshot=True)
    print("   Screenshot taken\n")
    
    # Example 4: Static method - no instance needed
    print("4. Using static method (no PlaywrightActions instance needed)...")
    path = PlaywrightActions.take_os_screenshot("screenshots/static_method.png")
    print(f"   Saved to: {path}\n")
    
    # Example 5: Element screenshot with optional page
    print("5. Taking element screenshot...")
    # actions.take_element_screenshot("#myElement", "screenshots/element.png")
    # Or with different page:
    # actions.take_element_screenshot("#myElement", "screenshots/element.png", page=other_page)
    print("   (Would use: actions.take_element_screenshot(selector, path, page=other_page))\n")


def example_use_cases():
    """Real-world use case examples."""
    
    print("=== Real-World Use Cases ===\n")
    
    print("Use Case 1: Screenshot on Locked Screen")
    print("-" * 50)
    print("Scenario: You need to capture evidence even when screen is locked")
    print("Solution: Use ScreenshotUtils.take_screenshot()")
    print("Code:")
    print("  from framework.utils import ScreenshotUtils")
    print("  path = ScreenshotUtils.take_screenshot('evidence.png')")
    print()
    
    print("Use Case 2: Multi-Monitor Testing")
    print("-" * 50)
    print("Scenario: Test application spans multiple monitors")
    print("Solution: Capture all monitors or specific monitor")
    print("Code:")
    print("  # Capture all monitors")
    print("  ScreenshotUtils.take_screenshot(monitor=0)")
    print("  # Capture primary monitor")
    print("  ScreenshotUtils.take_screenshot(monitor=1)")
    print("  # Capture secondary monitor")
    print("  ScreenshotUtils.take_screenshot(monitor=2)")
    print()
    
    print("Use Case 3: Screenshot Without Browser")
    print("-" * 50)
    print("Scenario: Need screenshot but browser is not available")
    print("Solution: Use OS-level screenshot")
    print("Code:")
    print("  from framework.playwright_wrapper import PlaywrightActions")
    print("  path = PlaywrightActions.take_os_screenshot('no_browser.png')")
    print()
    
    print("Use Case 4: Testing with Multiple Pages")
    print("-" * 50)
    print("Scenario: Multiple browser tabs/pages need screenshots")
    print("Solution: Pass page parameter to screenshot methods")
    print("Code:")
    print("  actions = PlaywrightActions(page1)")
    print("  actions.take_screenshot('page1.png')  # Uses page1")
    print("  actions.take_screenshot('page2.png', page=page2)  # Uses page2")
    print("  actions.take_screenshot('page3.png', page=page3)  # Uses page3")
    print()


def example_error_handling():
    """Examples of error handling and edge cases."""
    
    print("=== Error Handling Examples ===\n")
    
    print("Example 1: Invalid monitor number")
    print("Code:")
    print("  try:")
    print("      ScreenshotUtils.take_screenshot(monitor=99)")
    print("  except Exception as e:")
    print("      print(f'Error: {e}')")
    print()
    
    print("Example 2: Creating directories automatically")
    print("Code:")
    print("  # Directories are created automatically")
    print("  path = ScreenshotUtils.take_screenshot('path/to/deep/folder/screenshot.png')")
    print("  # The directory 'path/to/deep/folder/' will be created if it doesn't exist")
    print()
    
    print("Example 3: Screenshot with timestamp")
    print("Code:")
    print("  from datetime import datetime")
    print("  timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')")
    print("  path = ScreenshotUtils.take_screenshot(f'screenshot_{timestamp}.png')")
    print()


if __name__ == "__main__":
    """
    Note: This is an example file showing usage patterns.
    
    To run OS-level screenshot examples:
        python screenshot_examples.py
    
    To use Playwright examples, you need to have a page object:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://example.com")
            example_playwright_screenshots(page)
            browser.close()
    """
    
    print("\n" + "="*60)
    print("Screenshot Utility Examples")
    print("="*60 + "\n")
    
    # Run OS-level examples (no browser needed)
    example_os_level_screenshots()
    
    # Show use cases
    example_use_cases()
    
    # Show error handling
    example_error_handling()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")
    
    print("Note: Playwright examples require a browser and page object.")
    print("See the docstring in this file for more information.")

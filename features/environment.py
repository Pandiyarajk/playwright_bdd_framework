"""
Behave environment hooks and setup.
This file contains before/after hooks for scenario, feature, and test run lifecycle.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add framework to path
framework_path = Path(__file__).parent.parent
sys.path.insert(0, str(framework_path))

from framework.config.config_manager import ConfigManager
from framework.playwright_wrapper.browser_manager import BrowserManager
from framework.playwright_wrapper.playwright_actions import PlaywrightActions
from framework.logging_setup.logger import setup_logger
from framework.logging_setup.system_monitor import SystemMonitor
from framework.integrations.jira_integration import JiraIntegration
from framework.integrations.zephyr_integration import ZephyrIntegration
from framework.reporting.email_reporter import EmailReporter


def before_all(context):
    """
    Runs once before all features.
    Initialize framework-level resources.
    """
    # Setup configuration
    context.config_manager = ConfigManager()
    
    # Setup logging
    context.logger = setup_logger(context.config_manager)
    context.logger.info("=" * 80)
    context.logger.info("STARTING TEST EXECUTION")
    context.logger.info("=" * 80)
    
    # Initialize system monitor
    if context.config_manager.get('system_monitoring', 'enabled', True):
        context.system_monitor = SystemMonitor(context.config_manager)
        context.system_monitor.start()
        context.system_monitor.log_system_info()
        context.logger.info("System monitoring started")
    
    # Initialize Jira integration
    if context.config_manager.get('jira', 'enabled', False):
        try:
            context.jira_client = JiraIntegration(context.config_manager)
            context.logger.info("Jira integration initialized")
        except Exception as e:
            context.logger.warning(f"Failed to initialize Jira integration: {e}")
            context.jira_client = None
    else:
        context.jira_client = None
    
    # Initialize Zephyr Scale integration
    if context.config_manager.get('zephyr', 'enabled', False):
        try:
            context.zephyr_client = ZephyrIntegration(context.config_manager)
            context.logger.info("Zephyr Scale integration initialized")
        except Exception as e:
            context.logger.warning(f"Failed to initialize Zephyr Scale integration: {e}")
            context.zephyr_client = None
    else:
        context.zephyr_client = None
    
    # Test execution tracking
    context.test_results = {
        'passed': 0,
        'failed': 0,
        'skipped': 0,
        'total': 0,
        'start_time': datetime.now(),
        'scenarios': []
    }
    
    # Create directories
    for directory in ['reports', 'logs', 'screenshots', 'traces']:
        Path(directory).mkdir(parents=True, exist_ok=True)


def before_feature(context, feature):
    """Runs before each feature."""
    context.logger.info(f"\nSTARTING FEATURE: {feature.name}")
    context.logger.info(f"Tags: {feature.tags}")


def before_scenario(context, scenario):
    """Runs before each scenario."""
    context.logger.info(f"\n{'='*60}")
    context.logger.info(f"SCENARIO: {scenario.name}")
    context.logger.info(f"Tags: {scenario.tags}")
    context.logger.info(f"{'='*60}")
    
    # Initialize browser for scenario
    context.browser_manager = BrowserManager(context.config_manager)
    context.page = context.browser_manager.start_browser()
    context.actions = PlaywrightActions(context.page)
    
    # Store scenario start time
    context.scenario_start_time = datetime.now()
    
    # Extract test case ID from tags (e.g., @TC-123)
    context.test_case_id = None
    for tag in scenario.tags:
        if tag.startswith('TC-') or tag.startswith('tc-'):
            context.test_case_id = tag.upper()
            context.logger.info(f"Test Case ID: {context.test_case_id}")
            break
    
    # Navigate to base URL if configured
    base_url = context.config_manager.get('framework', 'base_url')
    if base_url and base_url != 'https://example.com':
        try:
            context.actions.navigate(base_url)
            context.logger.info(f"Navigated to base URL: {base_url}")
        except Exception as e:
            context.logger.warning(f"Failed to navigate to base URL: {e}")


def after_scenario(context, scenario):
    """Runs after each scenario."""
    # Calculate duration
    duration = (datetime.now() - context.scenario_start_time).total_seconds()
    
    # Determine status
    status = 'passed' if scenario.status == 'passed' else 'failed'
    
    # Log result
    context.logger.info(f"\nSCENARIO {status.upper()}: {scenario.name}")
    context.logger.info(f"Duration: {duration:.2f}s")
    
    # Take screenshot on failure
    if scenario.status == 'failed':
        screenshot_on_failure = context.config_manager.get('reporting', 'screenshot_on_failure', True)
        
        if screenshot_on_failure:
            try:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_name = f"failure_{scenario.name.replace(' ', '_')}_{timestamp}.png"
                screenshot_path = Path('screenshots') / screenshot_name
                
                context.actions.take_screenshot(str(screenshot_path), full_page=True)
                context.logger.info(f"Screenshot saved: {screenshot_path}")
                
                # Attach to scenario for reporting
                scenario.screenshot_path = str(screenshot_path)
            except Exception as e:
                context.logger.error(f"Failed to take screenshot: {e}")
    
    # Update test results
    context.test_results['total'] += 1
    if scenario.status == 'passed':
        context.test_results['passed'] += 1
    elif scenario.status == 'failed':
        context.test_results['failed'] += 1
    else:
        context.test_results['skipped'] += 1
    
    # Store scenario result
    scenario_result = {
        'name': scenario.name,
        'status': status,
        'duration': duration,
        'tags': scenario.tags,
        'test_case_id': context.test_case_id,
        'feature': scenario.feature.name
    }
    
    if scenario.status == 'failed':
        scenario_result['error'] = str(scenario.exception) if hasattr(scenario, 'exception') else 'Unknown error'
        if hasattr(scenario, 'screenshot_path'):
            scenario_result['screenshot'] = scenario.screenshot_path
    
    context.test_results['scenarios'].append(scenario_result)
    
    # Update Zephyr Scale if enabled
    if context.zephyr_client and context.test_case_id:
        try:
            context.zephyr_client.update_test_execution(
                test_case_key=context.test_case_id,
                status='Pass' if status == 'passed' else 'Fail',
                comment=f"Automated test execution - Duration: {duration:.2f}s"
            )
            context.logger.info(f"Updated Zephyr Scale for {context.test_case_id}")
        except Exception as e:
            context.logger.error(f"Failed to update Zephyr Scale: {e}")
    
    # Close browser
    try:
        context.browser_manager.stop()
    except Exception as e:
        context.logger.error(f"Error closing browser: {e}")


def after_feature(context, feature):
    """Runs after each feature."""
    context.logger.info(f"\nCOMPLETED FEATURE: {feature.name}")


def after_all(context):
    """
    Runs once after all features.
    Cleanup and reporting.
    """
    # Calculate total duration
    context.test_results['end_time'] = datetime.now()
    total_duration = (context.test_results['end_time'] - context.test_results['start_time']).total_seconds()
    context.test_results['duration'] = total_duration
    
    # Stop system monitor
    if hasattr(context, 'system_monitor'):
        context.system_monitor.stop()
        context.logger.info("System monitoring stopped")
    
    # Log summary
    context.logger.info("\n" + "=" * 80)
    context.logger.info("TEST EXECUTION SUMMARY")
    context.logger.info("=" * 80)
    context.logger.info(f"Total Scenarios: {context.test_results['total']}")
    context.logger.info(f"Passed: {context.test_results['passed']}")
    context.logger.info(f"Failed: {context.test_results['failed']}")
    context.logger.info(f"Skipped: {context.test_results['skipped']}")
    context.logger.info(f"Duration: {total_duration:.2f}s")
    context.logger.info("=" * 80)
    
    # Send email report if enabled
    if context.config_manager.get('reporting', 'email_enabled', False):
        try:
            email_reporter = EmailReporter(context.config_manager)
            
            # Check if should send only on failure
            email_on_failure_only = context.config_manager.get('reporting', 'email_on_failure_only', True)
            
            if not email_on_failure_only or context.test_results['failed'] > 0:
                email_reporter.send_summary_report(context.test_results)
                context.logger.info("Email report sent")
        except Exception as e:
            context.logger.error(f"Failed to send email report: {e}")


def before_step(context, step):
    """Runs before each step."""
    context.logger.debug(f"STEP: {step.keyword} {step.name}")


def after_step(context, step):
    """Runs after each step."""
    if step.status == 'failed':
        context.logger.error(f"STEP FAILED: {step.keyword} {step.name}")
        if hasattr(step, 'exception'):
            context.logger.error(f"Error: {step.exception}")
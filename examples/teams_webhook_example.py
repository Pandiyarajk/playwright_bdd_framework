#!/usr/bin/env python
"""
Microsoft Teams Webhook Integration Examples.
Demonstrates how to send instant alerts to Microsoft Teams for test case status and duration.
"""

from teams_webhook import TeamsWebhook

# =============================================================================
# SETUP: Configure Your Webhook URL
# =============================================================================
# To get your webhook URL:
# 1. Go to your Microsoft Teams channel
# 2. Click the three dots (...) next to the channel name
# 3. Select "Connectors" or "Workflows"
# 4. Add "Incoming Webhook" connector
# 5. Provide a name and create the webhook
# 6. Copy the webhook URL provided

WEBHOOK_URL = "https://your-company.webhook.office.com/webhookb2/your-webhook-url"


# =============================================================================
# Example 1: Basic Message
# =============================================================================
def example_basic_message():
    """Send a basic alert message to Teams."""
    print("Example 1: Basic Message")
    print("-" * 50)
    
    # Initialize with your webhook URL
    webhook = TeamsWebhook(WEBHOOK_URL)
    
    # Send a simple message
    result = webhook.send_message(
        message_title="🚨 Alert",
        activity_title="System Monitor",
        activity_subtitle="Health Check",
        text_message="This is a test message!"
    )
    
    if result['success']:
        print("✅ Message sent successfully!")
    else:
        print(f"❌ Failed to send message: {result.get('error')}")
    print()


# =============================================================================
# Example 2: Test Case Status Alert
# =============================================================================
def example_test_case_alert():
    """Send a test case status alert with duration."""
    print("Example 2: Test Case Status Alert")
    print("-" * 50)
    
    webhook = TeamsWebhook(WEBHOOK_URL)
    
    # Send alert for a passed test
    result = webhook.send_test_alert(
        test_name="User Login Validation",
        status="passed",
        duration=5.23,
        test_case_id="TC-001",
        feature_name="Authentication",
        tags=["smoke", "login", "critical"]
    )
    
    if result['success']:
        print("✅ Test alert sent successfully!")
    else:
        print(f"❌ Failed to send alert: {result.get('error')}")
    print()


# =============================================================================
# Example 3: Failed Test Alert with Error
# =============================================================================
def example_failed_test_alert():
    """Send alert for a failed test with error details."""
    print("Example 3: Failed Test Alert")
    print("-" * 50)
    
    webhook = TeamsWebhook(WEBHOOK_URL)
    
    # Send alert for a failed test
    result = webhook.send_test_alert(
        test_name="Payment Processing Flow",
        status="failed",
        duration=12.45,
        test_case_id="TC-052",
        feature_name="Payment",
        error_message="AssertionError: Expected payment status to be 'Completed' but got 'Pending'",
        tags=["regression", "payment", "high-priority"]
    )
    
    if result['success']:
        print("✅ Failed test alert sent successfully!")
    else:
        print(f"❌ Failed to send alert: {result.get('error')}")
    print()


# =============================================================================
# Example 4: Test Execution Summary
# =============================================================================
def example_execution_summary():
    """Send a test execution summary alert."""
    print("Example 4: Test Execution Summary")
    print("-" * 50)
    
    webhook = TeamsWebhook(WEBHOOK_URL)
    
    # Send summary of test execution
    result = webhook.send_summary_alert(
        total=50,
        passed=45,
        failed=3,
        skipped=2,
        duration=328.75,
        pass_rate=90.0
    )
    
    if result['success']:
        print("✅ Summary alert sent successfully!")
    else:
        print(f"❌ Failed to send summary: {result.get('error')}")
    print()


# =============================================================================
# Example 5: Custom Message with Facts
# =============================================================================
def example_custom_message_with_facts():
    """Send a custom message with multiple facts."""
    print("Example 5: Custom Message with Facts")
    print("-" * 50)
    
    webhook = TeamsWebhook(WEBHOOK_URL)
    
    # Send custom message with facts
    result = webhook.send_message(
        message_title="📊 Performance Test Results",
        activity_title="Load Testing",
        activity_subtitle="Production Environment",
        text_message="Load test completed successfully with acceptable performance metrics.",
        color="#0078D4",  # Blue color
        facts={
            "Environment": "Production",
            "Users Simulated": "1000",
            "Duration": "30 minutes",
            "Avg Response Time": "245ms",
            "Success Rate": "99.8%",
            "Peak TPS": "850"
        }
    )
    
    if result['success']:
        print("✅ Custom message sent successfully!")
    else:
        print(f"❌ Failed to send message: {result.get('error')}")
    print()


# =============================================================================
# Example 6: Using in Configuration-based Framework
# =============================================================================
def example_framework_integration():
    """
    Example of how Teams webhook is integrated in the framework.
    This shows how it's automatically called in environment.py
    """
    print("Example 6: Framework Integration")
    print("-" * 50)
    print("""
    The Teams webhook is automatically integrated into the framework:
    
    1. Configuration (config.ini):
       [teams]
       enabled = true
       webhook_url = https://your-company.webhook.office.com/webhookb2/your-webhook-url
       send_on_test_complete = true
       send_on_test_failure = true
       send_summary = true
    
    2. Automatic alerts are sent:
       - After each test scenario (if enabled)
       - On test failures (always if enabled)
       - Summary after all tests complete
    
    3. To enable Teams alerts:
       a. Set 'enabled = true' in config.ini
       b. Add your webhook URL
       c. Run your tests normally: python run_tests.py
    
    4. Alerts include:
       - Test name and status
       - Execution duration
       - Test case ID (if tagged)
       - Feature name
       - Error messages (for failures)
       - Tags
    """)
    print()


# =============================================================================
# Example 7: Environment-specific Webhooks
# =============================================================================
def example_environment_specific():
    """Example of using different webhooks for different environments."""
    print("Example 7: Environment-specific Webhooks")
    print("-" * 50)
    
    import os
    
    # Different webhooks for different environments
    webhooks = {
        'dev': "https://your-company.webhook.office.com/webhookb2/dev-webhook-url",
        'test': "https://your-company.webhook.office.com/webhookb2/test-webhook-url",
        'staging': "https://your-company.webhook.office.com/webhookb2/staging-webhook-url",
        'prod': "https://your-company.webhook.office.com/webhookb2/prod-webhook-url"
    }
    
    # Get current environment
    env = os.environ.get('ENV', 'test')
    webhook_url = webhooks.get(env, webhooks['test'])
    
    print(f"Using webhook for environment: {env}")
    
    webhook = TeamsWebhook(webhook_url)
    
    result = webhook.send_message(
        message_title=f"🔧 Test Execution - {env.upper()}",
        activity_title="Environment-specific Alert",
        activity_subtitle=f"Running on {env} environment",
        text_message=f"Test suite is running on {env} environment",
        color="#FF6B6B" if env == 'prod' else "#4ECDC4"
    )
    
    if result['success']:
        print("✅ Environment-specific alert sent!")
    else:
        print(f"❌ Failed to send alert: {result.get('error')}")
    print()


# =============================================================================
# Main Function
# =============================================================================
def main():
    """Run all examples."""
    print("=" * 70)
    print("Microsoft Teams Webhook Integration Examples")
    print("=" * 70)
    print()
    
    print("⚠️  Note: Update WEBHOOK_URL at the top of this file with your actual webhook URL")
    print()
    
    # Uncomment the examples you want to run
    # example_basic_message()
    # example_test_case_alert()
    # example_failed_test_alert()
    # example_execution_summary()
    # example_custom_message_with_facts()
    example_framework_integration()
    # example_environment_specific()
    
    print("=" * 70)
    print("Examples completed!")
    print("=" * 70)


if __name__ == '__main__':
    main()

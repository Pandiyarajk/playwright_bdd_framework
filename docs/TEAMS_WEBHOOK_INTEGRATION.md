# Microsoft Teams Webhook Integration

## Overview

The Microsoft Teams Webhook integration allows you to send **instant alerts** to Microsoft Teams channels for test case status and duration. This provides real-time visibility into your test automation results directly in your team's collaboration platform.

## Features

✅ **Instant Test Alerts** - Get notified immediately when tests complete  
✅ **Status & Duration Tracking** - See test status (passed/failed/skipped) and execution time  
✅ **Rich Formatting** - Color-coded messages with structured data  
✅ **Test Summaries** - Comprehensive execution summaries after test runs  
✅ **Configurable** - Control which alerts to send and when  
✅ **Easy Setup** - Simple configuration in `config.ini`

## Table of Contents

1. [Setup](#setup)
2. [Configuration](#configuration)
3. [Usage](#usage)
4. [Examples](#examples)
5. [API Reference](#api-reference)
6. [Troubleshooting](#troubleshooting)

---

## Setup

### Step 1: Create Incoming Webhook in Microsoft Teams

1. Navigate to your desired Microsoft Teams channel
2. Click the **three dots (...)** next to the channel name
3. Select **"Connectors"** or **"Workflows"**
4. Search for and add the **"Incoming Webhook"** connector
5. Provide a name for your webhook (e.g., "Test Automation Alerts")
6. Optionally, upload an image/icon for the webhook
7. Click **"Create"**
8. **Copy the webhook URL** - you'll need this for configuration

### Step 2: Install Dependencies

The Teams integration uses the `pymsteams` package. Install it with:

```bash
pip install pymsteams
```

Or install all framework dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Configure the Framework

Edit `config/config.ini` and add/update the `[teams]` section:

```ini
[teams]
enabled = true
webhook_url = https://your-company.webhook.office.com/webhookb2/your-webhook-url
send_on_test_complete = true
send_on_test_failure = true
send_summary = true
```

---

## Configuration

### Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `false` | Enable/disable Teams webhook integration |
| `webhook_url` | string | (required) | Your Microsoft Teams incoming webhook URL |
| `send_on_test_complete` | boolean | `true` | Send alert after every test completes |
| `send_on_test_failure` | boolean | `true` | Send alert when a test fails |
| `send_summary` | boolean | `true` | Send execution summary after all tests |

### Example Configuration

```ini
[teams]
enabled = true
webhook_url = https://outlook.office.com/webhook/a1b2c3d4-1234-5678-90ab-cdef12345678@...
send_on_test_complete = false  # Only send on failures
send_on_test_failure = true    # Always send failures
send_summary = true             # Send summary at end
```

---

## Usage

### Automatic Integration (Recommended)

Once configured, the Teams webhook automatically sends alerts during test execution:

```bash
# Run your tests as normal
python run_tests.py

# Or with specific tags
python run_tests.py --tags smoke

# Or specific feature
python run_tests.py --feature features/login.feature
```

The framework will automatically:
- Send alerts after each test scenario (if configured)
- Send alerts on test failures (if configured)
- Send a comprehensive summary after all tests complete

### Manual Usage (Advanced)

You can also use the Teams webhook programmatically in your code:

```python
from teams_webhook import TeamsWebhook

# Initialize with your webhook URL
webhook = TeamsWebhook("https://your-company.webhook.office.com/webhookb2/your-webhook-url")

# Send a basic message
result = webhook.send_message(
    message_title="🚨 Alert",
    activity_title="System Monitor",
    activity_subtitle="Health Check",
    text_message="This is a test message!"
)

# Send a test alert
result = webhook.send_test_alert(
    test_name="User Login Test",
    status="passed",
    duration=5.23,
    test_case_id="TC-001",
    feature_name="Authentication"
)
```

---

## Examples

### Example 1: Basic Alert

```python
from teams_webhook import TeamsWebhook

webhook = TeamsWebhook("https://your-webhook-url")

webhook.send_message(
    message_title="🚨 Alert",
    activity_title="System Monitor",
    activity_subtitle="Health Check",
    text_message="This is a test message!"
)
```

**Result in Teams:**
```
🚨 Alert
System Monitor
Health Check
This is a test message!
```

### Example 2: Test Case Alert (Passed)

```python
webhook.send_test_alert(
    test_name="User Login Validation",
    status="passed",
    duration=5.23,
    test_case_id="TC-001",
    feature_name="Authentication",
    tags=["smoke", "login", "critical"]
)
```

**Result in Teams:**
```
✅ Test Passed: User Login Validation

Test Automation Alert
TC-001

Test execution completed with status: PASSED

Status: PASSED
Duration: 5.23s
Test Case ID: TC-001
Feature: Authentication
Tags: smoke, login, critical
```

### Example 3: Test Case Alert (Failed)

```python
webhook.send_test_alert(
    test_name="Payment Processing",
    status="failed",
    duration=12.45,
    test_case_id="TC-052",
    feature_name="Payment",
    error_message="AssertionError: Expected status 'Completed' but got 'Pending'",
    tags=["regression", "payment"]
)
```

**Result in Teams:**
```
❌ Test Failed: Payment Processing

Test Automation Alert
TC-052

Test execution completed with status: FAILED

Error:
AssertionError: Expected status 'Completed' but got 'Pending'

Status: FAILED
Duration: 12.45s
Test Case ID: TC-052
Feature: Payment
Tags: regression, payment
```

### Example 4: Execution Summary

```python
webhook.send_summary_alert(
    total=50,
    passed=45,
    failed=3,
    skipped=2,
    duration=328.75,
    pass_rate=90.0
)
```

**Result in Teams:**
```
✅ Test Execution PASSED

Test Execution Summary
Executed 50 test scenarios

Test automation execution completed.

Overall Status: PASSED

Total Tests: 50
✅ Passed: 45
❌ Failed: 3
⏭️ Skipped: 2
Pass Rate: 90.0%
Duration: 328.75s
```

### Example 5: Custom Message with Facts

```python
webhook.send_message(
    message_title="📊 Performance Test Results",
    activity_title="Load Testing",
    activity_subtitle="Production Environment",
    text_message="Load test completed successfully.",
    color="#0078D4",
    facts={
        "Environment": "Production",
        "Users": "1000",
        "Avg Response": "245ms",
        "Success Rate": "99.8%"
    }
)
```

---

## API Reference

### TeamsWebhook Class

#### Constructor

```python
TeamsWebhook(webhook_url: str)
```

**Parameters:**
- `webhook_url` (str): Microsoft Teams incoming webhook URL

**Example:**
```python
webhook = TeamsWebhook("https://your-webhook-url")
```

---

#### send_message()

Send a general message to Microsoft Teams.

```python
webhook.send_message(
    message_title: str,
    activity_title: Optional[str] = None,
    activity_subtitle: Optional[str] = None,
    text_message: Optional[str] = None,
    color: Optional[str] = None,
    facts: Optional[Dict[str, str]] = None
) -> Dict[str, Any]
```

**Parameters:**
- `message_title` (str, required): Main title of the message
- `activity_title` (str, optional): Activity section title
- `activity_subtitle` (str, optional): Activity section subtitle
- `text_message` (str, optional): Main text content
- `color` (str, optional): Theme color (hex color code, e.g., `#FF0000`)
- `facts` (dict, optional): Dictionary of key-value pairs to display

**Returns:**
- `dict`: `{"success": True/False, "error": "error message if failed"}`

**Example:**
```python
result = webhook.send_message(
    message_title="🚨 Alert",
    text_message="System health check failed",
    color="#dc3545",
    facts={"CPU": "85%", "Memory": "92%"}
)

if result['success']:
    print("Message sent!")
else:
    print(f"Error: {result['error']}")
```

---

#### send_test_alert()

Send a test case status alert.

```python
webhook.send_test_alert(
    test_name: str,
    status: str,
    duration: float,
    test_case_id: Optional[str] = None,
    feature_name: Optional[str] = None,
    error_message: Optional[str] = None,
    tags: Optional[list] = None
) -> Dict[str, Any]
```

**Parameters:**
- `test_name` (str, required): Name of the test/scenario
- `status` (str, required): Test status (`passed`, `failed`, `skipped`)
- `duration` (float, required): Execution duration in seconds
- `test_case_id` (str, optional): Test case identifier (e.g., `TC-001`)
- `feature_name` (str, optional): Feature name
- `error_message` (str, optional): Error message if test failed
- `tags` (list, optional): List of test tags

**Returns:**
- `dict`: `{"success": True/False, "error": "error message if failed"}`

**Example:**
```python
result = webhook.send_test_alert(
    test_name="Login Test",
    status="passed",
    duration=3.45,
    test_case_id="TC-001",
    feature_name="Authentication",
    tags=["smoke", "critical"]
)
```

---

#### send_summary_alert()

Send a test execution summary.

```python
webhook.send_summary_alert(
    total: int,
    passed: int,
    failed: int,
    skipped: int,
    duration: float,
    pass_rate: float
) -> Dict[str, Any]
```

**Parameters:**
- `total` (int, required): Total number of tests
- `passed` (int, required): Number of passed tests
- `failed` (int, required): Number of failed tests
- `skipped` (int, required): Number of skipped tests
- `duration` (float, required): Total execution duration in seconds
- `pass_rate` (float, required): Pass rate percentage

**Returns:**
- `dict`: `{"success": True/False, "error": "error message if failed"}`

**Example:**
```python
result = webhook.send_summary_alert(
    total=100,
    passed=95,
    failed=3,
    skipped=2,
    duration=450.5,
    pass_rate=95.0
)
```

---

## Troubleshooting

### Issue: Messages Not Appearing in Teams

**Solution:**
1. Verify the webhook URL is correct in `config.ini`
2. Check that the webhook hasn't been deleted or disabled in Teams
3. Ensure `enabled = true` in the `[teams]` section
4. Check logs for error messages

### Issue: Import Error for pymsteams

**Solution:**
```bash
pip install pymsteams
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Webhook URL Not Found

**Solution:**
1. Verify you've created an Incoming Webhook connector in Teams
2. Copy the complete webhook URL (it should be very long)
3. Ensure no extra spaces or line breaks in the URL

### Issue: Messages Appear but Format is Wrong

**Solution:**
- Microsoft Teams has rate limits (1 message per second per webhook)
- If sending many messages quickly, add delays between sends
- Check that your webhook URL is valid and not expired

### Testing the Integration

Run the example script to test your setup:

```bash
python examples/teams_webhook_example.py
```

This will show you various examples and help verify your configuration.

---

## Color Codes

Use these hex color codes for different message types:

| Color | Hex Code | Use Case |
|-------|----------|----------|
| 🟢 Green | `#28a745` | Success, Passed tests |
| 🔴 Red | `#dc3545` | Failure, Critical alerts |
| 🟡 Yellow | `#ffc107` | Warnings, Skipped tests |
| 🔵 Blue | `#0078D4` | Information, General alerts |
| 🟣 Purple | `#6f42c1` | Special events |
| 🟠 Orange | `#fd7e14` | Performance issues |

---

## Best Practices

1. **Don't Spam**: Configure alerts wisely to avoid notification fatigue
   - Consider `send_on_test_complete = false` for large test suites
   - Always send failures: `send_on_test_failure = true`

2. **Use Test Case IDs**: Tag your scenarios with test case IDs for better tracking
   ```gherkin
   @TC-001 @smoke
   Scenario: User Login
   ```

3. **Multiple Webhooks**: Use different webhooks for different environments
   - Development team channel
   - QA team channel
   - Management dashboard channel

4. **Error Handling**: The integration handles errors gracefully
   - Failed webhook sends don't crash test execution
   - Errors are logged for debugging

5. **Rate Limits**: Microsoft Teams has rate limits
   - Maximum 1 message per second per webhook
   - Plan accordingly for large test suites

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review example code in `examples/teams_webhook_example.py`
3. Check logs in `logs/automation.log`
4. Verify Microsoft Teams webhook is active

---

## Related Documentation

- [Microsoft Teams Incoming Webhooks](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- [pymsteams Documentation](https://pypi.org/project/pymsteams/)
- Framework Email Integration: `docs/EMAIL_INTEGRATION.md`
- Framework Jira Integration: See `framework/integrations/jira_integration.py`

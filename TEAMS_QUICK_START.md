# Microsoft Teams Integration - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Create Teams Webhook (2 minutes)

1. Open Microsoft Teams and go to your channel
2. Click the **three dots (...)** next to channel name
3. Select **"Connectors"** or **"Workflows"**
4. Search for and add **"Incoming Webhook"**
5. Give it a name like "Test Automation Alerts"
6. Click **"Create"**
7. **Copy the webhook URL** (looks like: `https://your-company.webhook.office.com/webhookb2/...`)

### Step 2: Configure Framework (30 seconds)

Edit `config/config.ini`:

```ini
[teams]
enabled = true
webhook_url = YOUR_WEBHOOK_URL_HERE
send_on_test_complete = true
send_on_test_failure = true
send_summary = true
```

### Step 3: Install & Run (30 seconds)

```bash
# Install dependency
pip install pymsteams

# Run your tests
python3 run_tests.py
```

**Done!** 🎉 You'll now get instant alerts in Teams!

---

## 📊 What You'll See in Teams

### When a test passes:
```
✅ Test Passed: User Login Test
Duration: 3.2s | Status: PASSED | Test Case: TC-001
```

### When a test fails:
```
❌ Test Failed: Payment Processing
Duration: 8.5s | Status: FAILED | Test Case: TC-042
Error: AssertionError: Expected 'Completed' but got 'Pending'
```

### After all tests complete:
```
📊 Test Execution Summary
Total: 50 | ✅ Passed: 45 | ❌ Failed: 3 | ⏭️ Skipped: 2
Pass Rate: 90.0% | Duration: 245.8s
```

---

## 🔧 Configuration Tips

### For Large Test Suites (Reduce Noise):
```ini
send_on_test_complete = false  # Don't send every completion
send_on_test_failure = true    # Always send failures
send_summary = true             # Get final summary
```

### For Small/Critical Suites:
```ini
send_on_test_complete = true   # Send all completions
send_on_test_failure = true    # Send failures
send_summary = true             # Get final summary
```

---

## 💡 Quick Test

Test your webhook manually:

```python
from teams_webhook import TeamsWebhook

webhook = TeamsWebhook("YOUR_WEBHOOK_URL")
webhook.send_message(
    message_title="🚨 Test Alert",
    text_message="Teams integration is working!"
)
```

Or run the example:
```bash
python3 examples/teams_webhook_example.py
```

---

## 📚 Need More Details?

- **Full Documentation**: `docs/TEAMS_WEBHOOK_INTEGRATION.md`
- **Examples**: `examples/teams_webhook_example.py`
- **Implementation Summary**: `TEAMS_INTEGRATION_SUMMARY.md`

---

## ❓ Troubleshooting

**Messages not appearing?**
- ✓ Check webhook URL is correct
- ✓ Verify `enabled = true` in config
- ✓ Check webhook still exists in Teams

**Import errors?**
```bash
pip install pymsteams
```

**Want to test without running full test suite?**
```bash
python3 examples/teams_webhook_example.py
```

---

**That's it!** You're now getting instant test alerts in Microsoft Teams! 🎉

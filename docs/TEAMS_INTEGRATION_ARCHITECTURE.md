# Microsoft Teams Integration - Architecture & Flow

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Test Execution                            │
│                     (run_tests.py / behave)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    features/environment.py                       │
│  ┌────────────┐  ┌────────────┐  ┌──────────────────────────┐  │
│  │ before_all │  │after_scenario│ │     after_all           │  │
│  │    │       │  │     │       │  │        │                │  │
│  │    ▼       │  │     ▼       │  │        ▼                │  │
│  │ Initialize │  │  Send Test  │  │   Send Summary          │  │
│  │   Webhook  │  │   Alert     │  │     Alert               │  │
│  └────────────┘  └────────────┘  └──────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────┐
│              framework/integrations/teams_webhook.py             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              TeamsWebhook Class                         │   │
│  │                                                         │   │
│  │  ┌──────────────────┐  ┌─────────────────┐           │   │
│  │  │  send_message()  │  │send_test_alert()│           │   │
│  │  └──────────────────┘  └─────────────────┘           │   │
│  │           │                      │                     │   │
│  │           └──────────┬───────────┘                    │   │
│  │                      ▼                                 │   │
│  │          ┌─────────────────────┐                      │   │
│  │          │send_summary_alert() │                      │   │
│  │          └─────────────────────┘                      │   │
│  └──────────────────┬──────────────────────────────────┘   │
│                     │                                        │
└─────────────────────┼────────────────────────────────────────┘
                      │
                      ▼
        ┌──────────────────────────┐
        │      pymsteams           │
        │   (Python Library)       │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │  Microsoft Teams API     │
        │    (Webhook Endpoint)    │
        └────────────┬─────────────┘
                     │
                     ▼
        ┌──────────────────────────┐
        │   Microsoft Teams        │
        │   Channel Message        │
        └──────────────────────────┘
```

---

## 🔄 Data Flow

### Flow 1: Test Execution Alert

```
Test Scenario Completes
         │
         ▼
features/environment.py
  after_scenario() hook
         │
         ▼
Collects test data:
  - Test name
  - Status (pass/fail/skip)
  - Duration
  - Test case ID
  - Feature name
  - Error message (if failed)
  - Tags
         │
         ▼
Checks configuration:
  - send_on_test_complete?
  - send_on_test_failure?
         │
         ▼
context.teams_webhook
  .send_test_alert(...)
         │
         ▼
TeamsWebhook formats message:
  - Sets color (green/red/yellow)
  - Adds emoji (✅/❌/⏭️)
  - Structures facts
  - Formats error message
         │
         ▼
pymsteams.connectorcard()
  - Creates card
  - Adds sections
  - Adds facts
         │
         ▼
HTTP POST to Teams Webhook URL
         │
         ▼
Message appears in Teams Channel
```

### Flow 2: Execution Summary Alert

```
All Tests Complete
         │
         ▼
features/environment.py
  after_all() hook
         │
         ▼
Aggregates statistics:
  - Total tests
  - Passed count
  - Failed count
  - Skipped count
  - Total duration
  - Pass rate %
         │
         ▼
Checks configuration:
  - send_summary enabled?
         │
         ▼
context.teams_webhook
  .send_summary_alert(...)
         │
         ▼
TeamsWebhook formats summary:
  - Overall status color
  - Summary emoji
  - Statistics facts
         │
         ▼
pymsteams.connectorcard()
         │
         ▼
HTTP POST to Teams
         │
         ▼
Summary appears in Teams
```

---

## 📦 Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Configuration Layer                         │
│                                                                  │
│  config/config.ini                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ [teams]                                                   │  │
│  │ enabled = true                                            │  │
│  │ webhook_url = https://...                                 │  │
│  │ send_on_test_complete = true                              │  │
│  │ send_on_test_failure = true                               │  │
│  │ send_summary = true                                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Initialization Layer                          │
│                                                                  │
│  framework/integrations/teams_webhook.py                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ create_teams_webhook(config_manager)                      │  │
│  │   │                                                       │  │
│  │   ├─> Reads config                                        │  │
│  │   ├─> Validates webhook URL                               │  │
│  │   └─> Returns TeamsWebhook instance                       │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Integration Layer                           │
│                                                                  │
│  features/environment.py                                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ before_all():                                             │  │
│  │   context.teams_webhook = create_teams_webhook()          │  │
│  │                                                           │  │
│  │ after_scenario():                                         │  │
│  │   if context.teams_webhook:                               │  │
│  │     context.teams_webhook.send_test_alert(...)            │  │
│  │                                                           │  │
│  │ after_all():                                              │  │
│  │   if context.teams_webhook:                               │  │
│  │     context.teams_webhook.send_summary_alert(...)         │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Business Logic Layer                        │
│                                                                  │
│  framework/integrations/teams_webhook.py                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ class TeamsWebhook:                                       │  │
│  │                                                           │  │
│  │   send_message()                                          │  │
│  │     - General purpose message sender                      │  │
│  │     - Custom title, text, color, facts                    │  │
│  │                                                           │  │
│  │   send_test_alert()                                       │  │
│  │     - Specialized for test results                        │  │
│  │     - Auto color/emoji based on status                    │  │
│  │     - Formats duration, errors, tags                      │  │
│  │                                                           │  │
│  │   send_summary_alert()                                    │  │
│  │     - Specialized for execution summary                   │  │
│  │     - Aggregated statistics                               │  │
│  │     - Overall pass rate                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Transport Layer                             │
│                                                                  │
│  pymsteams library                                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ connectorcard(webhook_url)                                │  │
│  │   │                                                       │  │
│  │   ├─> .title()                                            │  │
│  │   ├─> .text()                                             │  │
│  │   ├─> .color()                                            │  │
│  │   ├─> .addSection()                                       │  │
│  │   │     └─> .addFact()                                    │  │
│  │   └─> .send()                                             │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      External Service                            │
│                                                                  │
│  Microsoft Teams                                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Incoming Webhook Connector                                │  │
│  │   │                                                       │  │
│  │   ├─> Receives HTTP POST                                  │  │
│  │   ├─> Validates webhook URL                               │  │
│  │   ├─> Formats message card                                │  │
│  │   └─> Posts to channel                                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Flow

```
                    ┌──────────────────────┐
                    │   Test Completes     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Teams Webhook        │
                    │ Enabled?             │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼ No                      ▼ Yes
          ┌──────────────┐        ┌────────────────┐
          │ Skip Alert   │        │ Check Status   │
          │ Continue     │        └────────┬───────┘
          └──────────────┘                 │
                                          │
                            ┌─────────────┴──────────────┐
                            │                            │
                            ▼ FAILED                     ▼ PASSED/SKIPPED
                    ┌──────────────────┐        ┌────────────────────┐
                    │ send_on_test_    │        │ send_on_test_      │
                    │ failure = true?  │        │ complete = true?   │
                    └───────┬──────────┘        └─────────┬──────────┘
                            │                             │
                            ▼ Yes                         ▼ Yes
                    ┌──────────────────┐        ┌────────────────────┐
                    │ Send Alert       │        │ Send Alert         │
                    │ (Red, ❌)        │        │ (Green/Yellow)     │
                    └──────────────────┘        └────────────────────┘


                    ┌──────────────────────┐
                    │ All Tests Complete   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Teams Webhook        │
                    │ Enabled?             │
                    └──────────┬───────────┘
                               │
                  ┌────────────┴────────────┐
                  │                         │
                  ▼ No                      ▼ Yes
          ┌──────────────┐        ┌────────────────┐
          │ Skip Summary │        │ send_summary   │
          └──────────────┘        │ = true?        │
                                 └────────┬───────┘
                                          │
                                          ▼ Yes
                                 ┌────────────────┐
                                 │ Send Summary   │
                                 │ Alert          │
                                 └────────────────┘
```

---

## 🔌 Integration Points

### Point 1: Initialization (before_all)
```python
# features/environment.py
def before_all(context):
    # ... other initializations ...
    
    # Initialize Teams webhook
    context.teams_webhook = create_teams_webhook(context.config_manager)
    if context.teams_webhook:
        logger.info("🔗 Teams webhook initialized")
```

### Point 2: Test Completion (after_scenario)
```python
# features/environment.py
def after_scenario(context, scenario):
    # ... calculate duration, status ...
    
    # Send Teams alert
    if context.teams_webhook:
        if should_send_alert(status, config):
            context.teams_webhook.send_test_alert(
                test_name=scenario.name,
                status=status,
                duration=duration,
                test_case_id=context.test_case_id,
                feature_name=scenario.feature.name,
                error_message=error_msg,
                tags=scenario.tags
            )
```

### Point 3: Execution Summary (after_all)
```python
# features/environment.py
def after_all(context):
    # ... aggregate results ...
    
    # Send Teams summary
    if context.teams_webhook and config.get('send_summary'):
        context.teams_webhook.send_summary_alert(
            total=total,
            passed=passed,
            failed=failed,
            skipped=skipped,
            duration=duration,
            pass_rate=pass_rate
        )
```

---

## 📊 Message Structure

### Test Alert Message Structure
```
┌─────────────────────────────────────────────────┐
│ 🎨 Color Bar (green/red/yellow based on status) │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Emoji] Status: Test Name                      │
│                                                 │
│  Test Automation Alert                          │
│  Test Case ID                                   │
│                                                 │
│  Test execution completed with status: [STATUS] │
│                                                 │
│  Error: [if failed]                             │
│  [error message]                                │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Facts                                    │  │
│  │ Status: PASSED/FAILED/SKIPPED            │  │
│  │ Duration: X.XXs                          │  │
│  │ Test Case ID: TC-XXX                     │  │
│  │ Feature: Feature Name                    │  │
│  │ Tags: tag1, tag2, tag3                   │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Summary Alert Message Structure
```
┌─────────────────────────────────────────────────┐
│ 🎨 Color Bar (based on overall status)          │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Emoji] Test Execution [STATUS]                │
│                                                 │
│  Test Execution Summary                         │
│  Executed N test scenarios                      │
│                                                 │
│  Test automation execution completed.           │
│  Overall Status: [STATUS]                       │
│                                                 │
│  ┌──────────────────────────────────────────┐  │
│  │ Facts                                    │  │
│  │ Total Tests: N                           │  │
│  │ ✅ Passed: N                             │  │
│  │ ❌ Failed: N                             │  │
│  │ ⏭️ Skipped: N                            │  │
│  │ Pass Rate: XX.X%                         │  │
│  │ Duration: XXX.XXs                        │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 🔐 Security Architecture

```
Configuration File               Environment Variable
(config.ini)                    (Optional Override)
     │                                │
     └────────────┬───────────────────┘
                  │
                  ▼
        ConfigManager reads webhook_url
                  │
                  ▼
        ┌─────────────────────┐
        │ Validation          │
        │ - URL format check  │
        │ - Not default value │
        │ - Not empty         │
        └─────────┬───────────┘
                  │
                  ▼
        TeamsWebhook instance created
                  │
                  ▼
        Stored in context (runtime only)
                  │
                  ▼
        Used for sending messages
        (HTTPS encrypted)
```

---

## 🚀 Execution Timeline

```
Time    Event                           Action
─────────────────────────────────────────────────────────────
0.0s    Test Suite Starts              → Initialize Teams webhook
                                       → Log: "Teams webhook initialized"

0.5s    Scenario 1 Starts              → (no Teams action)

5.2s    Scenario 1 Completes (PASS)    → Send test alert (if configured)
                                       → Message appears in Teams

5.5s    Scenario 2 Starts              → (no Teams action)

12.8s   Scenario 2 Completes (FAIL)    → Send test alert
                                       → Message appears in Teams

13.0s   Scenario 3 Starts              → (no Teams action)

...

325.5s  All Scenarios Complete         → Calculate summary statistics
                                       → Send summary alert
                                       → Summary appears in Teams

325.8s  Test Suite Ends                → Framework cleanup
```

---

## 📈 Scalability Considerations

```
┌────────────────────────────────────────────────────┐
│              Configuration Strategies               │
├────────────────────────────────────────────────────┤
│                                                    │
│ Small Test Suite (< 20 tests)                     │
│ ✓ send_on_test_complete = true                    │
│ ✓ send_on_test_failure = true                     │
│ ✓ send_summary = true                             │
│ Result: ~20 messages per run                      │
│                                                    │
│ Medium Test Suite (20-100 tests)                  │
│ ✓ send_on_test_complete = false                   │
│ ✓ send_on_test_failure = true                     │
│ ✓ send_summary = true                             │
│ Result: Failures + 1 summary                      │
│                                                    │
│ Large Test Suite (> 100 tests)                    │
│ ✓ send_on_test_complete = false                   │
│ ✓ send_on_test_failure = true (critical only)     │
│ ✓ send_summary = true                             │
│ Result: Critical failures + 1 summary             │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🔄 Error Handling Flow

```
send_test_alert() called
         │
         ▼
    try block
         │
         ├─> Create connector card
         │   ├─> Set title
         │   ├─> Set color
         │   ├─> Add sections
         │   ├─> Add facts
         │   └─> Send HTTP POST
         │       │
         │       ├─> Success
         │       │   ├─> Log success
         │       │   └─> Return {"success": True}
         │       │
         │       └─> HTTP Error
         │           └─> Raise exception
         │
         └─> Exception caught
             ├─> Log error with details
             ├─> Return {"success": False, "error": "..."}
             └─> Test execution continues normally
```

---

## 🎯 Summary

This architecture provides:

✅ **Separation of Concerns**: Each layer has a specific responsibility  
✅ **Fail-Safe Design**: Errors don't crash test execution  
✅ **Configurability**: Control behavior via config file  
✅ **Flexibility**: Can be used automatically or programmatically  
✅ **Scalability**: Handles test suites of any size  
✅ **Maintainability**: Clear integration points  
✅ **Security**: Webhook URL handling best practices  

The integration seamlessly fits into the existing framework while remaining modular and easy to maintain.

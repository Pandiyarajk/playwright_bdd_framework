# Powerlogger Migration Guide

## Overview

This document describes the migration from the standard Python `logging` module to `powerlogger` across the automation framework.

## What is Powerlogger?

Powerlogger is an enhanced logging library that provides:

- 🎨 **Colored console output** - Automatic color coding for different log levels
- 📁 **File logging** - Automatic file logging with rotation
- 😀 **Emoji support** - Native emoji support for more expressive logs
- ⚙️ **Zero configuration** - Works out of the box with sensible defaults
- 🔌 **Drop-in replacement** - Compatible with standard Python logging interface

## Changes Made

### 1. Requirements Update

Added `powerlogger` to `requirements.txt`:

```txt
powerlogger>=1.0.0
```

### 2. Core Logger Module

**File:** `framework/logging_setup/logger.py`

**Before:**
```python
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime
import colorlog

def setup_logger(config_manager=None):
    logger = logging.getLogger('AutomationFramework')
    # ... complex setup with handlers, formatters, etc.
```

**After:**
```python
from powerlogger import get_logger

def setup_logger(config_manager=None, name="AutomationFramework"):
    """
    Setup and configure logger using powerlogger.
    
    Args:
        config_manager: Configuration manager instance (optional, for backward compatibility)
        name: Logger name
        
    Returns:
        Powerlogger instance
    """
    logger = get_logger(name)
    return logger
```

### 3. Module Updates

All modules updated to use `powerlogger`:

#### System Monitor
**File:** `framework/logging_setup/system_monitor.py`
```python
from powerlogger import get_logger

class SystemMonitor:
    def __init__(self, config_manager=None):
        self.logger = get_logger('SystemMonitor')
```

#### Jira Integration
**File:** `framework/integrations/jira_integration.py`
```python
from powerlogger import get_logger

class JiraIntegration:
    def __init__(self, config_manager):
        self.logger = get_logger('JiraIntegration')
```

#### Zephyr Integration
**File:** `framework/integrations/zephyr_integration.py`
```python
from powerlogger import get_logger

class ZephyrIntegration:
    def __init__(self, config_manager):
        self.logger = get_logger('ZephyrIntegration')
```

#### Email Reporter
**File:** `framework/reporting/email_reporter.py`
```python
from powerlogger import get_logger

class EmailReporter:
    def __init__(self, config_manager):
        self.logger = get_logger('EmailReporter')
```

### 4. Test Environment

**File:** `features/environment.py`

Enhanced with emoji logging:

```python
def before_all(context):
    context.logger = setup_logger(context.config_manager)
    context.logger.info("=" * 80)
    context.logger.info("🚀 STARTING TEST EXECUTION")
    context.logger.info("=" * 80)
```

```python
def before_scenario(context, scenario):
    context.logger.info(f"🎬 SCENARIO: {scenario.name}")
    context.logger.info(f"🏷️ Tags: {scenario.tags}")
```

```python
def after_scenario(context, scenario):
    if status == 'passed':
        context.logger.info(f"✅ SCENARIO {status.upper()}: {scenario.name}")
    else:
        context.logger.error(f"❌ SCENARIO {status.upper()}: {scenario.name}")
```

### 5. Test Runner

**File:** `run_tests.py`

```python
from powerlogger import get_logger

logger = get_logger("test_runner")

def main():
    logger.info("🚀 Starting test execution script")
    # ... test execution logic
    logger.info("✅ Test execution completed successfully")
    logger.info("🏁 Test runner finished")
```

## Usage Examples

### Basic Usage

```python
from powerlogger import get_logger

logger = get_logger("my_module")

logger.info("🚀 Starting operation")
logger.debug("🔍 Debug details")
logger.warning("⚠️ Warning message")
logger.error("❌ Error occurred")
logger.info("✅ Operation completed")
```

### Exception Logging

```python
try:
    # Your code here
    logger.info("✅ Application running successfully")
except Exception as e:
    logger.error(f"❌ Application error: {e}")
    logger.exception("📋 Full traceback:")
```

### Test Execution Pattern

```python
logger.info("=" * 80)
logger.info("🚀 STARTING TEST EXECUTION")
logger.info("=" * 80)

logger.info("🎬 SCENARIO: User Login")
logger.debug("🔍 STEP: Navigate to page")
logger.info("✅ SCENARIO PASSED")
logger.info("⏱️ Duration: 2.45s")

logger.info("📋 TEST EXECUTION SUMMARY")
logger.info("✅ Passed: 5")
logger.info("❌ Failed: 1")
logger.info("🏁 EXECUTION COMPLETE")
```

## Emoji Reference

Common emojis used throughout the framework:

| Emoji | Meaning | Usage |
|-------|---------|-------|
| 🚀 | Start | Application/test start |
| ✅ | Success | Successful operations |
| ❌ | Error/Failure | Errors and failures |
| ⚠️ | Warning | Warnings |
| 🔍 | Debug | Debug information |
| 📋 | Info/List | Information, summaries |
| 📊 | Statistics | Metrics, reports |
| ⏱️ | Time | Duration, timing |
| 🎬 | Scenario | Test scenarios |
| 🏷️ | Tags | Test tags |
| 📸 | Screenshot | Screenshots |
| 🔗 | Integration | External integrations |
| 💾 | Data | Data operations |
| 🌐 | Network | Network/navigation |
| 🔢 | ID | Test case IDs |
| 📁 | Feature | Test features |
| 📧 | Email | Email operations |
| 🏁 | Finish | Completion |
| 🛑 | Stop | Stopping services |

## Benefits

1. **Cleaner Code**: Removed ~90 lines of logging configuration code
2. **Better Readability**: Emojis make logs more scannable
3. **Automatic Features**: File logging, rotation, colors all work automatically
4. **Consistent Styling**: All logs follow same color and format patterns
5. **Developer Experience**: Easier to spot important events in logs

## Migration Checklist

For migrating other modules:

- [ ] Import `get_logger` from `powerlogger`
- [ ] Replace `logging.getLogger(...)` with `get_logger(...)`
- [ ] Remove `import logging` if not needed elsewhere
- [ ] Add emojis to log messages for better readability
- [ ] Test the module to ensure logging works correctly

## Installation

```bash
pip install -r requirements.txt
```

Or install powerlogger directly:

```bash
pip install powerlogger
```

## Backwards Compatibility

The migration maintains backwards compatibility:

- `setup_logger()` function still exists and works
- All existing code using `context.logger` continues to work
- Log files are still created (powerlogger handles this automatically)
- All log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) work as before

## Additional Resources

- See `examples/powerlogger_example.py` for comprehensive usage examples
- Powerlogger documentation: [Link to powerlogger docs]
- Original logging code preserved in git history if needed

## Troubleshooting

### Import Error

**Error:** `ModuleNotFoundError: No module named 'powerlogger'`

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Emoji Display Issues

**Error:** Emojis not displaying correctly in terminal

**Solution:** Ensure your terminal supports UTF-8 encoding. Most modern terminals do by default.

### Log Files Not Created

**Error:** Expected log files not appearing

**Solution:** Powerlogger creates log files automatically. Check the default log directory or powerlogger configuration.

## Support

For issues or questions about the migration:
1. Check the example file: `examples/powerlogger_example.py`
2. Review this migration guide
3. Contact the framework maintainers

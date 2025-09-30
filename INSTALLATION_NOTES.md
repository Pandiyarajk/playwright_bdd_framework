# Installation Notes for Powerlogger Integration

## Quick Start

To use the powerlogger integration, you need to install the dependencies:

```bash
# Install all dependencies including powerlogger
pip install -r requirements.txt
```

Or install powerlogger specifically:

```bash
pip install powerlogger
```

## What is Powerlogger?

Powerlogger is a high-performance, thread-safe logging library for Python that enhances the standard logging module with:

- ✨ **Rich Console Output:** Colored and formatted console logs using the Rich library
- 🔒 **Thread-Safe Queue Logging:** Asynchronous, non-blocking log processing
- 📁 **File Rotation:** Automatic log file rotation based on size
- 😀 **UTF-8 Support:** Full support for Unicode and emoji characters
- ⚙️ **Easy Configuration:** Flexible configuration through config files
- 🪟 **Windows Optimization:** Special handling for Windows file access
- 🚀 **High Performance:** Optimized for real-time logging applications

## Verification

After installation, verify the integration:

```bash
python3 verify_powerlogger.py
```

This will test all imports and features to ensure everything is working correctly.

## Example Usage

Run the comprehensive example:

```bash
python3 examples/powerlogger_example.py
```

## Documentation

For complete information, see:

- `docs/POWERLOGGER_MIGRATION.md` - Migration guide
- `POWERLOGGER_INTEGRATION_SUMMARY.md` - Integration summary
- `examples/powerlogger_example.py` - Usage examples
- [PowerLogger on PyPI](https://pypi.org/project/powerlogger/) - Official package page

## Framework Integration Status

✅ All framework modules have been updated to use powerlogger:
- ✅ Core logging setup (`framework/logging_setup/logger.py`)
- ✅ System monitor (`framework/logging_setup/system_monitor.py`)
- ✅ Jira integration (`framework/integrations/jira_integration.py`)
- ✅ Zephyr integration (`framework/integrations/zephyr_integration.py`)
- ✅ Email reporter (`framework/reporting/email_reporter.py`)
- ✅ Test environment (`features/environment.py`)
- ✅ Test runner (`run_tests.py`)

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run verification: `python3 verify_powerlogger.py`
3. Run example: `python3 examples/powerlogger_example.py`
4. Review documentation in `docs/POWERLOGGER_MIGRATION.md`
5. Start using enhanced logging in your tests! 🎉

## Troubleshooting

### Module Not Found Error

**Error:** `ModuleNotFoundError: No module named 'powerlogger'`

**Solution:**
```bash
pip install powerlogger
# or
pip install -r requirements.txt
```

### Emoji Display Issues

**Issue:** Emojis not displaying correctly in terminal

**Solution:** Ensure your terminal supports UTF-8 encoding. Most modern terminals (Windows Terminal, iTerm2, GNOME Terminal, etc.) support this by default.

### Import Errors in Tests

**Issue:** Tests fail with import errors after migration

**Solution:** Make sure you've installed all dependencies and that your Python environment is activated:
```bash
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

pip install -r requirements.txt
```

## Support

For issues or questions:
- Check the documentation in `docs/POWERLOGGER_MIGRATION.md`
- Review the examples in `examples/powerlogger_example.py`
- Verify installation with `python3 verify_powerlogger.py`
- Contact the framework maintainers

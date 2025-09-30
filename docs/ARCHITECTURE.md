# Framework Architecture Documentation

## Overview

This document provides a comprehensive overview of the Playwright Python BDD Framework architecture, design patterns, and implementation details.

## Directory Structure

```
playwright-bdd-framework/
│
├── config/                          # Configuration files
│   ├── config.ini                  # Main configuration (INI format)
│   ├── dev.json                    # Development environment config
│   ├── test.json                   # Test environment config
│   └── staging.json                # Staging environment config
│
├── features/                        # BDD feature files and steps
│   ├── environment.py              # Behave hooks and setup
│   ├── steps/                      # Step definitions
│   │   ├── __init__.py
│   │   └── common_steps.py         # Common reusable steps
│   └── *.feature                   # Gherkin feature files
│
├── framework/                       # Core framework code
│   ├── __init__.py
│   │
│   ├── config/                     # Configuration management
│   │   ├── __init__.py
│   │   └── config_manager.py       # Config loader (INI/JSON/ENV)
│   │
│   ├── data_providers/             # Test data access layer
│   │   ├── __init__.py
│   │   ├── base_provider.py        # Abstract base class
│   │   ├── excel_provider.py       # Excel data provider
│   │   ├── json_provider.py        # JSON data provider
│   │   ├── csv_provider.py         # CSV data provider
│   │   ├── txt_provider.py         # Text file provider
│   │   └── sql_provider.py         # SQL providers (MS SQL, SQLite)
│   │
│   ├── playwright_wrapper/         # Playwright abstractions
│   │   ├── __init__.py
│   │   ├── browser_manager.py      # Browser lifecycle management
│   │   └── playwright_actions.py   # Reusable action wrappers
│   │
│   ├── utils/                      # Utility functions
│   │   ├── __init__.py
│   │   ├── date_utils.py           # Date manipulation functions
│   │   ├── ocr_utils.py            # OCR text extraction
│   │   ├── image_utils.py          # Image comparison/manipulation
│   │   ├── coordinate_utils.py     # Coordinate-based interactions
│   │   ├── file_utils.py           # File operations
│   │   └── string_utils.py         # String manipulation
│   │
│   ├── reporting/                  # Report generation
│   │   ├── __init__.py
│   │   ├── html_reporter.py        # HTML report generator
│   │   └── email_reporter.py       # Email notification sender
│   │
│   ├── integrations/               # External integrations
│   │   ├── __init__.py
│   │   ├── jira_integration.py     # Jira API integration
│   │   └── zephyr_integration.py   # Zephyr Scale integration
│   │
│   └── logging_setup/              # Logging and monitoring
│       ├── __init__.py
│       ├── logger.py               # Logger configuration
│       └── system_monitor.py       # System resource monitoring
│
├── test_data/                       # Test data files
│   ├── excel/                      # Excel test data
│   ├── json/                       # JSON test data
│   ├── csv/                        # CSV test data
│   ├── txt/                        # Text file test data
│   └── images/                     # Reference images for comparison
│
├── reports/                         # Generated reports
├── logs/                           # Log files
├── screenshots/                    # Test screenshots
├── traces/                         # Playwright traces
│
├── docs/                           # Documentation
│   ├── ARCHITECTURE.md             # This file
│   ├── LOW_LEVEL_REQUIREMENTS_PLAN.md
│   └── QUICK_START.md
│
├── .env.example                    # Environment variables template
├── .gitignore                      # Git ignore rules
├── behave.ini                      # Behave configuration
├── README.md                       # Project README
├── requirements.txt                # Python dependencies
├── setup.py                        # Package setup script
└── run_tests.py                    # Test execution script
```

## Design Patterns

### 1. Page Object Model (Adaptable)

While not implemented by default, the framework supports the Page Object pattern:

```python
# example_pages/login_page.py
class LoginPage:
    def __init__(self, actions):
        self.actions = actions
        self.username_field = '#username'
        self.password_field = '#password'
        self.login_button = 'button#login'
    
    def login(self, username, password):
        self.actions.type_text(self.username_field, username)
        self.actions.type_text(self.password_field, password)
        self.actions.click(self.login_button)
```

### 2. Strategy Pattern (Data Providers)

Different data sources implement the same interface:

```python
class BaseDataProvider(ABC):
    @abstractmethod
    def get_data(self, **kwargs) -> Any:
        pass
    
    @abstractmethod
    def get_all_data(self) -> List[Dict[str, Any]]:
        pass

# Implementations: ExcelProvider, JsonProvider, SqlProvider, etc.
```

### 3. Factory Pattern (Browser Management)

Browser creation is abstracted:

```python
browser_manager = BrowserManager(config)
page = browser_manager.start_browser(browser_type='chromium')
```

### 4. Wrapper Pattern (Playwright Actions)

Playwright API is wrapped for consistency and convenience:

```python
actions = PlaywrightActions(page)
actions.wait_and_click('#button', timeout=5000)  # Wait + Click in one call
```

### 5. Context Manager Pattern

Resources are managed with context managers:

```python
with ExcelProvider('data.xlsx') as excel:
    data = excel.get_all_data()
# File automatically closed
```

## Component Interactions

### Test Execution Flow

```
┌──────────────────────────────────────────────────────────────┐
│ 1. Test Execution Start (behave command)                     │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 2. before_all() Hook                                         │
│    - Load configuration                                      │
│    - Setup logging                                          │
│    - Initialize system monitor                              │
│    - Connect to Jira/Zephyr (if enabled)                   │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 3. before_feature() Hook                                     │
│    - Log feature start                                       │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 4. before_scenario() Hook                                    │
│    - Start browser                                           │
│    - Initialize Playwright actions                           │
│    - Extract test case ID from tags                         │
│    - Navigate to base URL (if configured)                   │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 5. Execute Scenario Steps                                    │
│    - Parse Gherkin steps                                     │
│    - Match with step definitions                             │
│    - Execute actions via Playwright wrapper                  │
│    - Access test data via data providers                     │
│    - Use utilities (date, OCR, image) as needed             │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 6. after_scenario() Hook                                     │
│    - Take screenshot on failure                              │
│    - Calculate duration                                      │
│    - Store test results                                      │
│    - Update Zephyr Scale (if enabled)                        │
│    - Close browser                                           │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 7. after_feature() Hook                                      │
│    - Log feature completion                                  │
└───────────────────────────────┬──────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────┐
│ 8. after_all() Hook                                          │
│    - Stop system monitor                                     │
│    - Generate reports (HTML)                                 │
│    - Send email report (if enabled)                          │
│    - Log execution summary                                   │
└──────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Test Step → Step Definition → Data Provider → Data Source
                ↓                                    ↓
          Playwright Actions                  (Excel/SQL/JSON/CSV)
                ↓
            Browser
                ↓
          Application
                ↓
            Results → Reporting → HTML/Email/Logs
                          ↓
                   Jira/Zephyr (if enabled)
```

## Configuration Hierarchy

Configuration values are resolved in this order (highest to lowest priority):

1. **Environment Variables**: `os.getenv('BROWSER')` or `${BROWSER}` in config files
2. **Environment-Specific JSON**: `config/test.json` (based on `ENV` variable)
3. **Custom Config File**: If provided via `ConfigManager(config_file='...')`
4. **Default INI Config**: `config/config.ini`
5. **Code Defaults**: Hardcoded fallback values

### Example

```python
# If ENV=test and config.ini has browser=chromium
# and test.json has browser=firefox
# and environment variable BROWSER=webkit
# Result: webkit (highest priority)

config = ConfigManager(env='test')
browser = config.get('framework', 'browser')  # Returns 'webkit'
```

## Extension Points

### 1. Custom Step Definitions

Create `features/steps/custom_steps.py`:

```python
from behave import given, when, then

@when('I perform custom business logic')
def custom_step(context):
    # Access framework components
    context.actions.click('#element')
    
    # Access data providers
    from framework.data_providers import JsonProvider
    data = JsonProvider('test_data/custom.json')
    
    # Access utilities
    from framework.utils import DateUtils
    past_date = DateUtils.get_past_date(days=7)
```

### 2. Custom Data Providers

Extend `BaseDataProvider`:

```python
from framework.data_providers import BaseDataProvider

class CustomAPIProvider(BaseDataProvider):
    def __init__(self, api_url):
        super().__init__(api_url)
        self.api_url = api_url
    
    def get_data(self, endpoint):
        # Custom implementation
        response = requests.get(f"{self.api_url}/{endpoint}")
        return response.json()
    
    def get_all_data(self):
        # Custom implementation
        pass
```

### 3. Custom Reporters

Create custom report format:

```python
class CustomReporter:
    @staticmethod
    def generate_report(test_results, output_path):
        # Custom report generation logic
        pass
```

### 4. Additional Integrations

Add new integrations in `framework/integrations/`:

```python
class SlackIntegration:
    def __init__(self, config_manager):
        self.webhook_url = config_manager.get('slack', 'webhook_url')
    
    def send_notification(self, message):
        # Send to Slack
        pass
```

## Best Practices

### 1. Configuration Management

✅ **Do:**
- Store sensitive data in environment variables
- Use environment-specific config files
- Document all configuration options

❌ **Don't:**
- Hardcode credentials in code
- Commit sensitive data to version control

### 2. Test Data

✅ **Do:**
- Use data providers for external data
- Keep test data separate from test logic
- Version control test data files

❌ **Don't:**
- Embed test data in step definitions
- Share test data between independent tests

### 3. Step Definitions

✅ **Do:**
- Keep steps atomic and reusable
- Use descriptive step names
- Parameterize steps with variables

❌ **Don't:**
- Create steps that do too much
- Duplicate step logic
- Include technical details in Gherkin

### 4. Error Handling

✅ **Do:**
- Use try-except blocks for external calls
- Log errors with context
- Take screenshots on failure
- Provide clear error messages

❌ **Don't:**
- Silently catch and ignore exceptions
- Use bare except clauses
- Fail tests without clear reason

### 5. Waits and Synchronization

✅ **Do:**
- Use explicit waits (`wait_for_selector`)
- Set appropriate timeouts
- Wait for specific conditions

❌ **Don't:**
- Use `time.sleep()` for synchronization
- Set excessively long timeouts
- Assume elements are immediately available

## Performance Considerations

### 1. Browser Management

- **Reuse contexts** when possible to avoid browser startup overhead
- **Close browsers** properly to free resources
- **Use headless mode** in CI/CD for faster execution

### 2. Data Providers

- **Cache** frequently accessed data
- **Close connections** after use (use context managers)
- **Limit query results** with appropriate filters

### 3. Screenshots and Traces

- **Disable** in non-failure scenarios for speed
- **Compress** images if storage is a concern
- **Clean up** old artifacts periodically

### 4. Logging

- **Use appropriate log levels** (DEBUG only when needed)
- **Rotate logs** to prevent disk fill
- **Async logging** for high-volume scenarios

## Security Considerations

### 1. Credentials Management

- Store in environment variables or secret management tools
- Never commit to version control
- Rotate credentials regularly

### 2. Data Protection

- Don't log sensitive data (passwords, tokens, PII)
- Sanitize screenshots that may contain sensitive info
- Encrypt test data at rest if needed

### 3. Network Security

- Use TLS/SSL for all external connections
- Validate SSL certificates
- Use VPN for internal system access

## Troubleshooting Guide

### Common Issues

#### 1. Playwright Installation

**Problem:** Browsers not found  
**Solution:** Run `playwright install --with-deps`

#### 2. OCR Not Working

**Problem:** Tesseract not found  
**Solution:** Install Tesseract OCR for your OS

#### 3. Database Connection Failed

**Problem:** Cannot connect to MS SQL  
**Solution:** Check connection string, firewall, and ODBC driver

#### 4. Import Errors

**Problem:** Module not found  
**Solution:** Ensure virtual environment is activated and dependencies installed

#### 5. Test Timeout

**Problem:** Tests hang or timeout  
**Solution:** Increase timeout in config, check for infinite waits

## Maintenance

### Regular Tasks

1. **Update Dependencies**: `pip install -U -r requirements.txt`
2. **Update Browsers**: `playwright install`
3. **Clean Artifacts**: Remove old reports, screenshots, logs
4. **Review Logs**: Check for warnings or errors
5. **Update Documentation**: Keep docs in sync with code changes

### Monitoring

- Check system resource usage during test runs
- Review test execution times for performance degradation
- Monitor failure rates and patterns
- Track Jira/Zephyr integration success rates

## Future Enhancements

Potential additions to the framework:

1. **Parallel Execution**: Implement behave-parallel or custom solution
2. **API Testing**: Add REST API testing capabilities
3. **Mobile Testing**: Extend for mobile web and native apps
4. **Visual Regression**: Add pixel-perfect visual comparison
5. **Cloud Execution**: Support BrowserStack, Sauce Labs, etc.
6. **AI/ML**: Intelligent element locators, self-healing tests
7. **GraphQL Support**: Add GraphQL testing utilities
8. **WebSocket Testing**: Real-time communication testing
9. **Accessibility Testing**: Automated a11y checks
10. **Performance Metrics**: Capture and report page load times

## Contributing

When contributing to the framework:

1. Follow existing code structure and patterns
2. Add tests for new functionality
3. Update documentation
4. Use meaningful commit messages
5. Create pull requests for review

## License

MIT License - See LICENSE file for details

---

**Document Maintained By:** Automation Team  
**Last Updated:** September 30, 2025
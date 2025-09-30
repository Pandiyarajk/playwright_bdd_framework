# Playwright-Python BDD Framework — Low Level Requirements Plan

**Document Version:** 1.0  
**Date:** September 30, 2025  
**Status:** Final  
**Author:** Automation Team

---

## Table of Contents

1. [Document Purpose](#1-document-purpose)
2. [Goals and Non-Goals](#2-goals-and-non-goals)
3. [High-Level Architecture](#3-high-level-architecture)
4. [Component Details](#4-component-details)
5. [Test Data Support](#5-test-data-support)
6. [Configuration Management](#6-configuration-management)
7. [OCR and Image Recognition](#7-ocr-and-image-recognition)
8. [Reusable Functions](#8-reusable-functions)
9. [Reporting and Notifications](#9-reporting-and-notifications)
10. [Jira and Zephyr Scale Integration](#10-jira-and-zephyr-scale-integration)
11. [System Resources and OS Monitoring](#11-system-resources-and-os-monitoring)
12. [BDD and Tag Support](#12-bdd-and-tag-support)
13. [Deployment and Environment](#13-deployment-and-environment)
14. [Non-Functional Requirements](#14-non-functional-requirements)
15. [Acceptance Criteria](#15-acceptance-criteria)
16. [Dependencies and Prerequisites](#16-dependencies-and-prerequisites)

---

## 1. Document Purpose

This Low-Level Requirements Plan (LLRP) defines the functional and technical specifications for a **Playwright Python BDD Test Automation Framework**. The framework provides:

- BDD support using Behave
- Multiple test data sources (Excel, MS SQL, SQLite, JSON, CSV, TXT)
- OCR and image recognition capabilities
- Comprehensive reusable functions for date operations and Playwright interactions
- Multi-format reporting with email notifications
- Jira and Zephyr Scale integration
- System resource monitoring and logging
- Tag-based test execution
- Multi-environment configuration support

---

## 2. Goals and Non-Goals

### 2.1 Goals

1. **Maintainable Framework**: Provide a well-structured, modular framework that is easy to maintain and extend
2. **BDD Support**: Enable behavior-driven development with Gherkin syntax using Behave
3. **Data Flexibility**: Support multiple test data sources for maximum flexibility
4. **Visual Testing**: Provide OCR and image comparison capabilities for visual validation
5. **Comprehensive Utilities**: Offer rich date manipulation and coordinate-based interaction functions
6. **Enterprise Integration**: Integrate with Jira and Zephyr Scale for test management
7. **Observability**: Log system resources and provide detailed execution reports
8. **Multi-Environment**: Support configuration for different environments (dev, test, staging, production)

### 2.2 Non-Goals

1. **Not a Test Management Tool**: Framework integrates with existing tools (Jira/Zephyr) but doesn't replace them
2. **Not a Commercial OCR Engine**: Uses open-source Tesseract; doesn't include commercial OCR licenses
3. **Not a Performance Testing Tool**: Focused on functional test automation, not load/performance testing
4. **Not a Mobile Testing Framework**: Designed for web browser testing (though Playwright supports mobile viewports)

---

## 3. High-Level Architecture

### 3.1 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Test Execution Layer                     │
│  ┌───────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ Behave Runner │──│ Feature Files│──│ Step Definitions  │   │
│  └───────────────┘  └──────────────┘  └───────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Framework Core Layer                        │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │ Config Mgr   │  │ Playwright    │  │ Utilities        │    │
│  │ (INI/JSON)   │  │ Wrapper       │  │ (Date/OCR/Image) │    │
│  └──────────────┘  └───────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Data & Integration Layer                    │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │ Data         │  │ Jira/Zephyr   │  │ System Monitor   │    │
│  │ Providers    │  │ Integration   │  │ & Logger         │    │
│  └──────────────┘  └───────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Reporting Layer                            │
│  ┌──────────────┐  ┌───────────────┐  ┌──────────────────┐    │
│  │ HTML Reports │  │ Behave/Allure │  │ Email Reporter   │    │
│  └──────────────┘  └───────────────┘  └──────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### 3.2 Component Responsibilities

| Component | Responsibility |
|-----------|---------------|
| **Test Execution** | BDD scenario execution, test orchestration |
| **Framework Core** | Configuration, browser management, utilities |
| **Data & Integration** | Test data access, external system integration |
| **Reporting** | Test result collection, report generation, notifications |

---

## 4. Component Details

### 4.1 Test Runner Layer

**File:** `features/environment.py`, `run_tests.py`

**Requirements:**

- **FR-001**: Support Behave as the BDD test runner
- **FR-002**: Provide hooks for test lifecycle events (before/after scenario, feature, all)
- **FR-003**: Support command-line execution with various parameters
- **FR-004**: Enable tag-based test filtering
- **FR-005**: Support parallel execution capability

**Implementation Details:**

```python
# Command-line interface
python run_tests.py --tags smoke --browser chromium --headless

# Behave hooks
def before_all(context):     # Framework initialization
def before_feature(context, feature):
def before_scenario(context, scenario):
def after_scenario(context, scenario):
def after_feature(context, feature):
def after_all(context):      # Cleanup and reporting
```

### 4.2 Configuration Manager

**File:** `framework/config/config_manager.py`

**Requirements:**

- **FR-010**: Load configuration from INI files
- **FR-011**: Load configuration from JSON files
- **FR-012**: Support environment variables with `${VAR_NAME}` substitution
- **FR-013**: Support multi-environment configurations (dev, test, staging, prod)
- **FR-014**: Provide hierarchical configuration override (defaults < file < env vars)

**Configuration Sources (Priority Order):**

1. Environment variables (highest priority)
2. Environment-specific JSON (`dev.json`, `test.json`)
3. Custom config file (if specified)
4. Default INI config (`config.ini`)

**API Examples:**

```python
config = ConfigManager(env='test')
browser = config.get('framework', 'browser', default='chromium')
base_url = config.get('framework', 'base_url')
all_config = config.get_all()
```

### 4.3 Browser Manager

**File:** `framework/playwright_wrapper/browser_manager.py`

**Requirements:**

- **FR-020**: Support Chromium, Firefox, and WebKit browsers
- **FR-021**: Support headless and headed modes
- **FR-022**: Configure viewport dimensions
- **FR-023**: Manage browser context and pages
- **FR-024**: Support tracing for debugging

**API Examples:**

```python
browser_manager = BrowserManager(config)
page = browser_manager.start_browser(browser_type='chromium', headless=True)
new_page = browser_manager.new_page()
browser_manager.close_browser()
```

### 4.4 Playwright Actions Wrapper

**File:** `framework/playwright_wrapper/playwright_actions.py`

**Requirements:**

- **FR-030**: Provide wrapper functions for all common Playwright actions
- **FR-031**: Support coordinate-based clicking and interaction
- **FR-032**: Provide robust wait and assertion methods
- **FR-033**: Support frame, dialog, and cookie operations
- **FR-034**: Enable JavaScript execution
- **FR-035**: Support file upload and download operations

**Category:** Navigation, Interaction, Waiting, Assertions, Screenshots

**API Examples:**

```python
actions = PlaywrightActions(page)
actions.navigate('https://example.com')
actions.click('#submit-button')
actions.type_text('#username', 'testuser')
actions.wait_and_click('#confirm-button', timeout=5000)
actions.assert_visible('#success-message')
actions.take_screenshot('page.png')
```

---

## 5. Test Data Support

### 5.1 Data Provider Architecture

**Files:** `framework/data_providers/*.py`

**Requirements:**

- **FR-040**: Abstract data provider interface for all data sources
- **FR-041**: Excel support (.xlsx, .xls) with openpyxl and xlrd
- **FR-042**: MS SQL Server support with pyodbc/pymssql
- **FR-043**: SQLite support with built-in sqlite3
- **FR-044**: JSON support with dot-notation key access
- **FR-045**: CSV support with header detection
- **FR-046**: Text file support with line-based access
- **FR-047**: Context manager support for automatic resource cleanup

### 5.2 Excel Provider

**File:** `framework/data_providers/excel_provider.py`

**Capabilities:**

```python
excel = ExcelProvider('test_data/users.xlsx')

# Get specific cell
value = excel.get_data(sheet='Sheet1', row=2, column='A')

# Get entire row as dictionary
row_data = excel.get_data(sheet='Sheet1', row=2, row_as_dict=True)
# Returns: {'Name': 'John', 'Email': 'john@example.com', ...}

# Get all data
all_data = excel.get_all_data(sheet='Sheet1', has_header=True)

# Get sheet names
sheets = excel.get_sheet_names()
```

### 5.3 SQL Providers

**Files:** `framework/data_providers/sql_provider.py`

**MS SQL Server:**

```python
sql_server = SqlServerProvider(
    server='localhost',
    database='testdb',
    username='user',
    password='pass'
)

# Execute query
users = sql_server.get_data('SELECT * FROM users WHERE active = ?', (True,))

# Get single value
count = sql_server.get_single_value('SELECT COUNT(*) FROM users')

# Execute non-query
sql_server.execute('UPDATE users SET status = ? WHERE id = ?', ('active', 1))
```

**SQLite:**

```python
sqlite = SqliteProvider('test_data/test.db')
users = sqlite.get_all_data('users')
tables = sqlite.get_tables()
```

### 5.4 JSON Provider

**File:** `framework/data_providers/json_provider.py`

**Capabilities:**

```python
json_data = JsonProvider('test_data/config.json')

# Dot-notation access
api_url = json_data.get_data('api.endpoint.url')

# Array indexing
first_user = json_data.get_data('users[0].name')

# Filter data
admins = json_data.get_by_filter(lambda x: x.get('role') == 'admin')

# Find by key-value
user = json_data.get_by_key_value('id', 123)
```

### 5.5 CSV and Text Providers

**CSV Provider:**

```python
csv = CsvProvider('test_data/users.csv', has_header=True)
all_rows = csv.get_all_data()
filtered = csv.get_by_column_value('status', 'active')
```

**Text Provider:**

```python
txt = TxtProvider('test_data/data.txt')
lines = txt.get_lines()
search_results = txt.search('pattern', case_sensitive=False)
```

---

## 6. Configuration Management

### 6.1 Configuration Files

**config.ini** - Main configuration

```ini
[framework]
browser = chromium
headless = false
base_url = https://example.com
timeout = 30000

[jira]
enabled = true
server = https://company.atlassian.net
api_token = ${JIRA_TOKEN}

[zephyr]
enabled = true
api_token = ${ZEPHYR_TOKEN}
test_cycle_key = PROJ-C123

[reporting]
screenshot_on_failure = true
email_enabled = true

[email]
smtp_server = smtp.gmail.com
smtp_port = 587
from_email = automation@company.com
to_emails = team@company.com

[ocr]
engine = tesseract
language = eng
confidence_threshold = 60

[system_monitoring]
enabled = true
log_interval_seconds = 60
```

**Environment-Specific JSON** (e.g., `test.json`)

```json
{
  "framework": {
    "base_url": "https://test.example.com",
    "headless": true
  },
  "database": {
    "ms_sql_server": "test-db-server.example.com",
    "ms_sql_database": "testdb_test"
  }
}
```

**.env** - Sensitive credentials

```bash
JIRA_TOKEN=your_jira_token
ZEPHYR_TOKEN=your_zephyr_token
DB_PASSWORD=your_db_password
SMTP_PASSWORD=your_smtp_password
```

---

## 7. OCR and Image Recognition

### 7.1 OCR Utilities

**File:** `framework/utils/ocr_utils.py`

**Requirements:**

- **FR-050**: Extract text from images using Tesseract OCR
- **FR-051**: Support image preprocessing for better OCR accuracy
- **FR-052**: Provide text location coordinates
- **FR-053**: Support multiple languages
- **FR-054**: Filter results by confidence threshold
- **FR-055**: Extract specific data (numbers, emails, etc.)

**Capabilities:**

```python
ocr = OCRUtils(language='eng', config='--psm 6')

# Extract text
text = ocr.extract_text('captcha.png', preprocess=True)

# Get text with details (position, confidence)
details = ocr.extract_text_with_details('screenshot.png')
for item in details:
    print(f"{item['text']} at ({item['left']}, {item['top']}) - {item['confidence']}%")

# Find text location
location = ocr.find_text_location('page.png', 'Login')
# Returns: {'text': 'Login', 'x': 100, 'y': 200, 'confidence': 95}

# Verify text presence
has_text = ocr.verify_text_present('screenshot.png', 'Welcome')

# Extract numbers only
numbers = ocr.extract_numbers('invoice.png')
```

### 7.2 Image Utilities

**File:** `framework/utils/image_utils.py`

**Requirements:**

- **FR-060**: Compare two images for similarity
- **FR-061**: Support multiple comparison methods (SSIM, MSE, Histogram)
- **FR-062**: Find smaller image within larger image (template matching)
- **FR-063**: Highlight differences between images
- **FR-064**: Crop, resize, and convert images
- **FR-065**: Wait for image to appear on screen

**Capabilities:**

```python
img_utils = ImageUtils()

# Compare images
result = img_utils.compare_images('expected.png', 'actual.png', 
                                  method='ssim', threshold=0.95)
print(f"Match: {result['match']}, Similarity: {result['similarity']}")

# Find image in image
location = img_utils.find_image_in_image('screenshot.png', 'button.png', 
                                         confidence=0.8)
if location:
    print(f"Button found at ({location['x']}, {location['y']})")

# Highlight differences
diff_img = img_utils.highlight_differences('v1.png', 'v2.png', 
                                          color=(0, 0, 255))

# Wait for image
found = img_utils.wait_for_image('reference.png', screenshot_func, 
                                 timeout=30, confidence=0.9)
```

### 7.3 Coordinate Utilities

**File:** `framework/utils/coordinate_utils.py`

**Requirements:**

- **FR-070**: Get element coordinates and bounding box
- **FR-071**: Click at specific coordinates
- **FR-072**: Drag and drop by coordinates
- **FR-073**: Check if element is in viewport
- **FR-074**: Calculate distances between points
- **FR-075**: Get relative positions between elements

**Capabilities:**

```python
coord_utils = CoordinateUtils()

# Get element center coordinates
coords = coord_utils.get_element_coordinates(locator)
# Returns: {'x': 100, 'y': 200, 'left': 50, 'top': 150, 'width': 100, 'height': 100}

# Click at coordinates
coord_utils.click_at_coordinates(page, x=100, y=200, button='left')

# Drag and drop
coord_utils.drag_and_drop_coordinates(page, from_x=50, from_y=50, 
                                      to_x=200, to_y=200, steps=10)

# Check if in viewport
is_visible = coord_utils.is_element_in_viewport(locator)

# Calculate distance
distance = coord_utils.calculate_distance(x1=0, y1=0, x2=100, y2=100)

# Get relative position
rel_pos = coord_utils.get_element_relative_position(element, reference)
# Returns: {'offset_x': 50, 'offset_y': 30, 'is_above': False, ...}
```

---

## 8. Reusable Functions

### 8.1 Date Utilities

**File:** `framework/utils/date_utils.py`

**Requirements:**

- **FR-080**: Get current date/time with formatting
- **FR-081**: Calculate past dates (days, weeks, months, years)
- **FR-082**: Calculate future dates (days, weeks, months, years)
- **FR-083**: Compare dates (greater, less, equal)
- **FR-084**: Calculate date differences in various units
- **FR-085**: Format and parse dates flexibly
- **FR-086**: Check business days and weekends
- **FR-087**: Get start/end of month
- **FR-088**: Unix timestamp conversion
- **FR-089**: Humanize dates (e.g., "2 days ago")

**Comprehensive API:**

```python
date_utils = DateUtils()

# Current date
now = date_utils.get_current_date('%Y-%m-%d')

# Past dates
past = date_utils.get_past_date(days=7, weeks=2, months=1, years=0, 
                                format_string='%Y-%m-%d')

# Future dates
future = date_utils.get_future_date(months=3, format_string='%Y-%m-%d')

# Comparisons
is_greater = date_utils.is_date_greater('2024-12-31', '2024-01-01')  # True
is_equal = date_utils.is_date_equal('2024-01-01', '2024-01-01')      # True

# Difference
days_diff = date_utils.get_date_difference('2024-12-31', '2024-01-01', 
                                           unit='days')     # 365
months_diff = date_utils.get_date_difference('2024-12-31', '2024-01-01', 
                                             unit='months') # 12

# Format conversion
formatted = date_utils.format_date('2024-01-15', '%d/%m/%Y', 
                                   input_format='%Y-%m-%d')

# Flexible parsing
date_obj = date_utils.parse_date('Jan 15, 2024')  # Auto-detects format

# Day of week
day = date_utils.get_day_of_week('2024-01-15')  # 'Monday'

# Business day checks
is_weekend = date_utils.is_weekend('2024-01-13')      # True (Saturday)
is_business = date_utils.is_business_day('2024-01-15')  # True (Monday)
next_business = date_utils.get_next_business_day()

# Month boundaries
start = date_utils.get_start_of_month()  # First day of current month
end = date_utils.get_end_of_month()      # Last day of current month

# Timestamps
timestamp = date_utils.get_timestamp(milliseconds=True)
date_from_ts = date_utils.from_timestamp(timestamp, milliseconds=True)

# Humanize
human = date_utils.humanize_date('2024-01-01')  # '11 months ago'
```

### 8.2 String Utilities

**File:** `framework/utils/string_utils.py`

**Capabilities:**

- Generate random strings, emails
- Remove special characters
- Extract numbers, emails from text
- Truncate, normalize whitespace
- Case conversions (snake_case, camelCase)

### 8.3 File Utilities

**File:** `framework/utils/file_utils.py`

**Capabilities:**

- Create, delete directories and files
- Copy, move files
- List files with patterns
- Read/write JSON
- Get file metadata

---

## 9. Reporting and Notifications

### 9.1 Logging System

**File:** `framework/logging_setup/logger.py`

**Requirements:**

- **FR-090**: Support multiple log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- **FR-091**: Log to console with color coding
- **FR-092**: Log to file with rotation (10MB max, 5 backups)
- **FR-093**: Configurable log format and datetime format
- **FR-094**: Separate log files per test run with timestamp

**Log Format:**

```
2024-09-30 10:15:30 - AutomationFramework - INFO - Starting test execution
2024-09-30 10:15:31 - AutomationFramework - DEBUG - Browser launched: chromium
2024-09-30 10:15:32 - AutomationFramework - ERROR - Element not found: #submit-btn
```

### 9.2 HTML Report

**File:** `framework/reporting/html_reporter.py`

**Requirements:**

- **FR-100**: Generate modern, responsive HTML reports
- **FR-101**: Display test metrics (total, passed, failed, skipped, pass rate)
- **FR-102**: Show execution summary (start time, end time, duration)
- **FR-103**: List all scenarios with status
- **FR-104**: Include error details for failures
- **FR-105**: Visual progress bar and color-coded status

**Report Sections:**

1. **Header**: Overall status, progress bar
2. **Metrics**: Total, Passed, Failed, Skipped, Pass Rate
3. **Summary**: Start/End time, Duration
4. **Scenarios**: Detailed results for each scenario
5. **Footer**: Generation timestamp

### 9.3 Email Reporter

**File:** `framework/reporting/email_reporter.py`

**Requirements:**

- **FR-110**: Send HTML email reports via SMTP
- **FR-111**: Support TLS/SSL encryption
- **FR-112**: Configurable recipients (multiple addresses)
- **FR-113**: Option to send only on failure
- **FR-114**: Attach screenshots and logs
- **FR-115**: Customizable subject prefix

**Email Content:**

- Execution status (PASSED/FAILED)
- Test metrics with color coding
- Scenario results
- Links to artifacts (if hosted)

### 9.4 Behave Integration

**Configuration:** `behave.ini`

**Supported Formats:**

- **pretty**: Colored console output
- **plain**: Simple text output
- **json**: JSON format for programmatic processing
- **junit**: JUnit XML for CI integration
- **allure**: Allure report format

---

## 10. Jira and Zephyr Scale Integration

### 10.1 Jira Integration

**File:** `framework/integrations/jira_integration.py`

**Requirements:**

- **FR-120**: Connect to Jira Cloud using API token
- **FR-121**: Retrieve test case details by issue key
- **FR-122**: Create defects/bugs automatically on test failure
- **FR-123**: Add comments to issues
- **FR-124**: Add attachments (screenshots) to issues
- **FR-125**: Link test cases to defects
- **FR-126**: Transition issues to different statuses
- **FR-127**: Query test cases by labels/tags

**Configuration:**

```ini
[jira]
enabled = true
server = https://company.atlassian.net
email = automation@company.com
api_token = ${JIRA_TOKEN}
project_key = PROJ
create_defects_on_failure = false
```

**Usage in Tests:**

```gherkin
@TC-123
Scenario: Login test
  # Framework automatically retrieves TC-123 details
  # On failure, can create linked defect
```

**API Examples:**

```python
jira = JiraIntegration(config)

# Get issue
issue = jira.get_issue('PROJ-123')

# Create defect
defect_key = jira.create_defect(
    summary='Login button not working',
    description='Automated test failure in TC-123',
    test_case_key='TC-123',
    priority='High',
    screenshot_path='screenshots/failure.png'
)

# Add comment
jira.add_comment('PROJ-123', 'Automated test passed')

# Link issues
jira.link_issues('TC-123', 'BUG-456', link_type='Tested by')
```

### 10.2 Zephyr Scale Integration

**File:** `framework/integrations/zephyr_integration.py`

**Requirements:**

- **FR-130**: Connect to Zephyr Scale API
- **FR-131**: Retrieve test case and cycle details
- **FR-132**: Create test executions
- **FR-133**: Update test execution status (Pass, Fail, Blocked, Not Executed)
- **FR-134**: Add execution comments and actual results
- **FR-135**: Bulk update multiple executions
- **FR-136**: Get execution results summary
- **FR-137**: Update test cycle status

**Configuration:**

```ini
[zephyr]
enabled = true
api_token = ${ZEPHYR_TOKEN}
base_url = https://api.zephyrscale.smartbear.com/v2
test_cycle_key = PROJ-C123
update_test_execution = true
```

**Automatic Integration:**

1. Test scenarios tagged with `@TC-xxx` are mapped to Zephyr test cases
2. After scenario execution, result is pushed to Zephyr
3. Test cycle is updated with execution status

**API Examples:**

```python
zephyr = ZephyrIntegration(config)

# Get test case
test_case = zephyr.get_test_case('TC-123')

# Create execution
execution_id = zephyr.create_test_execution(
    test_case_key='TC-123',
    status='Pass',
    comment='Automated execution - Duration: 5.2s',
    environment='test'
)

# Update execution
zephyr.update_test_execution('TC-123', status='Fail', 
                             comment='Login failed')

# Get results summary
summary = zephyr.get_test_results_summary('PROJ-C123')
print(f"Pass rate: {summary['pass_rate']}%")
```

---

## 11. System Resources and OS Monitoring

### 11.1 System Monitor

**File:** `framework/logging_setup/system_monitor.py`

**Requirements:**

- **FR-140**: Capture system information (OS, architecture, CPU, memory, disk)
- **FR-141**: Monitor CPU usage (overall and per core)
- **FR-142**: Monitor memory usage (used, available, percentage)
- **FR-143**: Monitor disk usage (used, free, percentage)
- **FR-144**: Monitor network I/O (bytes sent/received)
- **FR-145**: Log metrics at configurable intervals
- **FR-146**: Run monitoring in background thread
- **FR-147**: Capture process-specific metrics

**System Information Logged:**

```
SYSTEM INFORMATION
==============================================================================
Platform: Linux 6.12.8+
Architecture: x86_64
Processor: Intel(R) Core(TM) i7-9750H CPU @ 2.60GHz
Python Version: 3.10.12
Hostname: test-runner-01
CPU Cores: 6 physical, 12 logical
Total Memory: 16.00 GB
Total Disk: 500.00 GB
==============================================================================
```

**Periodic Metrics:**

```
System Metrics - 2024-09-30T10:15:30 | CPU: 45.2% | Memory: 62.5% (10.00GB used, 6.00GB available) | Disk: 75.0% (375.00GB used, 125.00GB free) | Network: 150.23MB sent, 320.45MB received
```

**Configuration:**

```ini
[system_monitoring]
enabled = true
log_system_info = true
log_interval_seconds = 60
capture_cpu = true
capture_memory = true
capture_disk = true
capture_network = true
```

---

## 12. BDD and Tag Support

### 12.1 Feature Files

**Location:** `features/*.feature`

**Gherkin Syntax:**

```gherkin
@smoke @regression
Feature: User Authentication
  As a user
  I want to log in
  So that I can access my account

  Background:
    Given I navigate to the login page

  @TC-101 @critical
  Scenario: Successful login
    When I enter "testuser" in "#username"
    And I enter "password123" in "#password"
    And I click "button#login"
    Then I should be on "/dashboard"
    And I should see ".user-profile"

  @TC-102 @negative
  Scenario: Failed login with invalid credentials
    When I enter "testuser" in "#username"
    And I enter "wrongpassword" in "#password"
    And I click "button#login"
    Then I should see ".error-message"
    And ".error-message" should contain text "Invalid credentials"
```

### 12.2 Tag Support

**Requirements:**

- **FR-150**: Support multiple tags per scenario (@smoke, @regression, etc.)
- **FR-151**: Filter tests by tag expressions (AND, OR, NOT)
- **FR-152**: Map test case IDs to scenarios (@TC-123)
- **FR-153**: Support priority tags (@critical, @high, @medium, @low)
- **FR-154**: Support category tags (@api, @ui, @integration)

**Tag Usage:**

```bash
# Run smoke tests only
behave --tags=@smoke

# Run smoke AND regression
behave --tags="@smoke and @regression"

# Run smoke OR api tests
behave --tags="@smoke or @api"

# Run all except skip tagged
behave --tags="~@skip"

# Run critical priority tests
behave --tags=@critical

# Complex expression
behave --tags="(@smoke or @regression) and ~@skip"
```

### 12.3 Step Definitions

**Location:** `features/steps/common_steps.py`

**Comprehensive Step Library:**

**Navigation:**
- `Given I navigate to "{url}"`
- `When I reload the page`
- `When I go back`

**Interaction:**
- `When I click "{selector}"`
- `When I enter "{text}" in "{selector}"`
- `When I select "{option}" from "{selector}"`
- `When I check "{selector}"`
- `When I hover over "{selector}"`
- `When I drag "{source}" to "{target}"`
- `When I upload "{file}" to "{selector}"`

**Coordinates:**
- `When I click at coordinates ({x}, {y})`

**Waiting:**
- `When I wait for "{selector}" to be visible`
- `When I wait for {seconds} seconds`
- `When I wait for page to load`

**Assertions:**
- `Then I should see "{selector}"`
- `Then I should not see "{selector}"`
- `Then "{selector}" should contain text "{text}"`
- `Then the page URL should be "{url}"`
- `Then the page title should contain "{title}"`

**Screenshots:**
- `When I take a screenshot`
- `When I take a screenshot named "{name}"`

**Scroll:**
- `When I scroll to "{selector}"`
- `When I scroll to the bottom`

---

## 13. Deployment and Environment

### 13.1 Local Development

**Prerequisites:**

- Python 3.8+
- pip
- git

**Setup:**

```bash
# Clone repository
git clone <repo-url>
cd playwright-bdd-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Tesseract (for OCR)
# Ubuntu: sudo apt-get install tesseract-ocr
# Mac: brew install tesseract
# Windows: Download from GitHub

# Configure
cp .env.example .env
# Edit .env with your credentials
```

### 13.2 CI/CD Integration

**GitHub Actions Example:**

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install --with-deps
          sudo apt-get install -y tesseract-ocr
      
      - name: Run tests
        run: python run_tests.py --tags smoke --headless
        env:
          ENV: test
          JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
          ZEPHYR_TOKEN: ${{ secrets.ZEPHYR_TOKEN }}
      
      - name: Upload artifacts
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: |
            reports/
            screenshots/
            logs/
```

**Jenkins Pipeline Example:**

```groovy
pipeline {
    agent any
    
    environment {
        ENV = 'test'
        JIRA_TOKEN = credentials('jira-api-token')
        ZEPHYR_TOKEN = credentials('zephyr-api-token')
    }
    
    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt'
                sh '. venv/bin/activate && playwright install --with-deps'
            }
        }
        
        stage('Test') {
            steps {
                sh '. venv/bin/activate && python run_tests.py --tags smoke --headless'
            }
        }
    }
    
    post {
        always {
            archiveArtifacts artifacts: 'reports/**, screenshots/**, logs/**', allowEmptyArchive: true
            junit 'reports/junit/*.xml'
        }
    }
}
```

### 13.3 Docker Support

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps

# Copy framework
COPY . .

# Run tests
CMD ["python", "run_tests.py", "--headless"]
```

**docker-compose.yml:**

```yaml
version: '3.8'

services:
  tests:
    build: .
    environment:
      - ENV=test
      - BROWSER=chromium
      - HEADLESS=true
      - JIRA_TOKEN=${JIRA_TOKEN}
      - ZEPHYR_TOKEN=${ZEPHYR_TOKEN}
    volumes:
      - ./reports:/app/reports
      - ./screenshots:/app/screenshots
      - ./logs:/app/logs
```

---

## 14. Non-Functional Requirements

### 14.1 Performance

- **NFR-001**: Framework initialization should complete within 5 seconds
- **NFR-002**: Test execution overhead should be < 10% of actual test time
- **NFR-003**: Screenshot capture should complete within 2 seconds
- **NFR-004**: Data provider queries should return within 5 seconds

### 14.2 Scalability

- **NFR-010**: Support concurrent execution of 10+ tests (with parallel runners)
- **NFR-011**: Handle test suites with 1000+ scenarios
- **NFR-012**: Support data files up to 100MB
- **NFR-013**: Maintain performance with 500+ screenshots per run

### 14.3 Reliability

- **NFR-020**: Automatic retry for transient failures (network, element timing)
- **NFR-021**: Graceful error handling with detailed error messages
- **NFR-022**: Resource cleanup even on unexpected failures
- **NFR-023**: 99% framework stability (no framework bugs causing test failures)

### 14.4 Maintainability

- **NFR-030**: Modular architecture with clear separation of concerns
- **NFR-031**: Comprehensive inline documentation
- **NFR-032**: Consistent code style (PEP 8 compliant)
- **NFR-033**: 80%+ code coverage for framework components

### 14.5 Usability

- **NFR-040**: Clear error messages with actionable guidance
- **NFR-041**: Comprehensive documentation with examples
- **NFR-042**: Command-line interface with intuitive options
- **NFR-043**: Quick start guide for new users

### 14.6 Security

- **NFR-050**: Credentials stored in environment variables, not in code
- **NFR-051**: Support for credential management tools (e.g., Vault)
- **NFR-052**: No sensitive data in logs or reports
- **NFR-053**: Secure SMTP connection with TLS/SSL

---

## 15. Acceptance Criteria

### 15.1 Configuration

- ✅ Framework loads configuration from INI, JSON, and environment variables
- ✅ Environment-specific configurations override defaults correctly
- ✅ `${VAR_NAME}` substitution works in configuration files
- ✅ All configuration options are documented

### 15.2 Browser Automation

- ✅ Tests run successfully on Chromium, Firefox, and WebKit
- ✅ Headless and headed modes work correctly
- ✅ Screenshots and traces are captured on failure
- ✅ All Playwright wrapper methods function as expected

### 15.3 Data Providers

- ✅ Excel files (.xlsx, .xls) can be read with header detection
- ✅ MS SQL Server connection and queries work
- ✅ SQLite database operations function correctly
- ✅ JSON files support dot-notation and filtering
- ✅ CSV files parse with correct delimiter detection
- ✅ Text files support line-based access and search

### 15.4 OCR and Image Recognition

- ✅ Text extraction from images works with >80% accuracy
- ✅ Image comparison identifies matches with >95% accuracy
- ✅ Template matching locates sub-images correctly
- ✅ Coordinate-based clicking functions properly

### 15.5 Date Utilities

- ✅ All date calculation functions return correct results
- ✅ Date comparisons work correctly
- ✅ Format conversions handle various input formats
- ✅ Business day calculations are accurate

### 15.6 Reporting

- ✅ HTML reports generate with correct data and formatting
- ✅ Email reports send successfully with attachments
- ✅ Behave reports include all scenarios and steps
- ✅ Allure reports integrate correctly

### 15.7 Integrations

- ✅ Jira connection established and issues created/updated
- ✅ Zephyr Scale test executions pushed successfully
- ✅ Test case IDs mapped from scenario tags
- ✅ System metrics logged at configured intervals

### 15.8 BDD

- ✅ All common step definitions work correctly
- ✅ Tag filtering functions as expected
- ✅ Before/after hooks execute in correct order
- ✅ Test data accessible in scenario context

---

## 16. Dependencies and Prerequisites

### 16.1 Python Packages

**Core:**
- playwright >= 1.40.0
- behave >= 1.2.6

**Data Providers:**
- openpyxl >= 3.1.2
- xlrd >= 2.0.1
- pyodbc >= 5.0.1
- pymssql >= 2.2.11

**Image/OCR:**
- pytesseract >= 0.3.10
- Pillow >= 10.1.0
- opencv-python >= 4.8.1.78
- scikit-image >= 0.22.0

**Utilities:**
- python-dateutil >= 2.8.2
- arrow >= 1.3.0
- psutil >= 5.9.6

**Reporting:**
- behave-html-formatter >= 0.9.10
- allure-behave >= 2.13.2
- jinja2 >= 3.1.2

**Integrations:**
- jira >= 3.5.2
- requests >= 2.31.0

### 16.2 External Tools

**Required:**
- Tesseract OCR (for OCR functionality)

**Optional:**
- Allure CLI (for Allure reports)
- Docker (for containerized execution)

### 16.3 Services

**Required for Integration:**
- Jira Cloud instance
- Zephyr Scale subscription
- SMTP server (for email reports)

**Optional:**
- MS SQL Server (if using SQL data provider)

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Author | Automation Team | | 2025-09-30 |
| Reviewer | QA Lead | | |
| Approver | Engineering Manager | | |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-09-30 | Automation Team | Initial version |

---

**End of Document**
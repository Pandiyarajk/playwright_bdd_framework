# Playwright Python BDD Test Automation Framework

A comprehensive test automation framework built with Playwright and Python, supporting BDD (Behavior Driven Development) with behave, multiple test data sources, OCR/image recognition, and enterprise integrations.

## Features

### 🎭 Core Framework
- **Playwright Python**: Latest Playwright sync/async API support
- **BDD with Behave**: Gherkin syntax for readable test scenarios
- **Tag-based Execution**: Run tests by tags, features, scenarios

### 📊 Test Data Sources
- Excel (.xlsx, .xls)
- MS SQL Server
- SQLite
- JSON
- CSV
- TXT
- Environment Variables

### 🔧 Utilities
- **Date Functions**: Compare dates, get past/future dates, format conversions
- **OCR Support**: Text extraction from images using Tesseract
- **Image Recognition**: Compare images, find elements by image
- **Coordinate Actions**: Click by coordinates, get element positions
- **Element Wrappers**: Reusable Playwright element interaction functions

### 📈 Reporting
- Behave JSON/HTML reports
- Allure reports
- Custom HTML reports
- Email notifications
- Screenshot on failure

### 🔗 Integrations
- **Jira + Zephyr Scale**: Automatic test execution results push
- **System Monitoring**: CPU, memory, disk, network logging
- **OS Info**: Platform, version, environment details

### ⚙️ Configuration
- INI files
- JSON files
- Environment variables
- Multi-environment support (dev, test, staging, prod)

## Installation

### Prerequisites
- Python 3.8+
- pip

### Setup

```bash
# Clone repository
git clone <repository-url>
cd playwright-bdd-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install

# Install Tesseract OCR (for OCR features)
# Ubuntu/Debian: sudo apt-get install tesseract-ocr
# macOS: brew install tesseract
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
```

## Project Structure

```
playwright-bdd-framework/
├── config/                      # Configuration files
│   ├── config.ini              # Main configuration
│   ├── dev.json                # Environment-specific configs
│   └── test.json
├── features/                    # BDD feature files
│   ├── steps/                  # Step definitions
│   ├── environment.py          # Behave hooks
│   └── *.feature              # Gherkin scenarios
├── framework/                   # Core framework
│   ├── config/                 # Configuration manager
│   ├── data_providers/         # Test data providers
│   ├── playwright_wrapper/     # Playwright utilities
│   ├── utils/                  # Utility functions
│   ├── reporting/              # Report generators
│   ├── integrations/           # Jira, Zephyr, etc.
│   └── logging_setup/          # Logging configuration
├── test_data/                   # Test data files
│   ├── excel/
│   ├── json/
│   ├── csv/
│   └── images/
├── reports/                     # Generated reports
├── logs/                        # Log files
├── screenshots/                 # Test screenshots
└── requirements.txt            # Python dependencies
```

## Quick Start

### 1. Configure Framework

Edit `config/config.ini`:

```ini
[framework]
browser = chromium
headless = false
base_url = https://example.com

[reporting]
screenshot_on_failure = true
email_enabled = false

[jira]
enabled = false
```

### 2. Write a Feature

Create `features/example.feature`:

```gherkin
@smoke @regression
Feature: Login Functionality
  
  @TC-123
  Scenario: Successful login
    Given I open the application
    When I enter username "testuser"
    And I enter password "password123"
    And I click the login button
    Then I should see the dashboard
```

### 3. Run Tests

```bash
# Run all tests
behave

# Run with tags
behave --tags=@smoke

# Run specific feature
behave features/example.feature

# Generate Allure report
behave -f allure_behave.formatter:AllureFormatter -o allure-results
allure serve allure-results
```

## Usage Examples

### Date Utilities

```python
from framework.utils.date_utils import DateUtils

date_utils = DateUtils()

# Get past date
past_date = date_utils.get_past_date(days=7)  # 7 days ago

# Get future date
future_date = date_utils.get_future_date(days=30)  # 30 days from now

# Compare dates
is_greater = date_utils.compare_dates(date1, date2)  # Returns True if date1 > date2

# Format date
formatted = date_utils.format_date(date, "%Y-%m-%d")
```

### Data Providers

```python
from framework.data_providers import ExcelProvider, JsonProvider

# Excel data
excel = ExcelProvider("test_data/excel/users.xlsx")
data = excel.get_data(sheet="Sheet1", row=2)

# JSON data
json_provider = JsonProvider("test_data/json/config.json")
config = json_provider.get_data(key="api.endpoint")
```

### OCR and Image Recognition

```python
from framework.utils.ocr_utils import OCRUtils
from framework.utils.image_utils import ImageUtils

# Extract text from image
ocr = OCRUtils()
text = ocr.extract_text("screenshots/captcha.png")

# Compare images
img_utils = ImageUtils()
similarity = img_utils.compare_images("expected.png", "actual.png")
```

### Playwright Wrapper

```python
from framework.playwright_wrapper import PlaywrightActions

actions = PlaywrightActions(page)

# Click by coordinates
actions.click_by_coordinates(x=100, y=200)

# Wait and click
actions.wait_and_click("button#submit")

# Type with delay
actions.type_text("input#username", "testuser", delay=100)

# Take screenshot
actions.take_screenshot("login_page.png")
```

## Configuration

### Environment Variables

Create `.env` file:

```
ENV=test
BROWSER=chromium
HEADLESS=true
JIRA_TOKEN=your_token_here
ZEPHYR_TOKEN=your_token_here
DB_CONNECTION_STRING=your_connection_string
```

### Jira Integration

Configure in `config/config.ini`:

```ini
[jira]
enabled = true
server = https://your-domain.atlassian.net
email = your-email@example.com
api_token = ${JIRA_TOKEN}
project_key = PROJ

[zephyr]
enabled = true
api_token = ${ZEPHYR_TOKEN}
test_cycle_key = PROJ-C123
```

Test cases are mapped using tags: `@TC-123` maps to Jira test case `TC-123`

## Reporting

### Email Reports

Configure SMTP in `config/config.ini`:

```ini
[email]
enabled = true
smtp_server = smtp.gmail.com
smtp_port = 587
from_email = automation@example.com
to_emails = team@example.com,manager@example.com
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Support

For issues and questions, please create an issue in the repository.
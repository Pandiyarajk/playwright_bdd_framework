# Quick Start Guide

## Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd playwright-bdd-framework

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 2. Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and `config/config.ini` with your settings.

## Running Tests

### Basic Execution

```bash
# Run all tests
behave

# Run with specific tags
behave --tags=@smoke
behave --tags="@smoke and @regression"

# Run specific feature
behave features/example.feature
```

### Using the Test Runner Script

```bash
# Run all tests
python run_tests.py

# Run with tags
python run_tests.py --tags smoke

# Run in specific browser
python run_tests.py --browser firefox

# Run in headless mode
python run_tests.py --headless

# Run in specific environment
python run_tests.py --env dev

# Generate Allure report
python run_tests.py --allure
```

## Writing Tests

### 1. Create Feature File

Create `features/my_feature.feature`:

```gherkin
@smoke
Feature: My Feature
  
  @TC-123
  Scenario: Test something
    Given I navigate to "https://example.com"
    When I click "button#submit"
    Then I should see ".success-message"
```

### 2. Use Existing Step Definitions

The framework provides comprehensive step definitions in `features/steps/common_steps.py`:

- Navigation: `Given I navigate to "{url}"`
- Clicking: `When I click "{selector}"`
- Input: `When I enter "{text}" in "{selector}"`
- Assertions: `Then I should see "{selector}"`
- Waiting: `When I wait for {seconds} seconds`
- And many more...

### 3. Create Custom Step Definitions

Create `features/steps/my_steps.py`:

```python
from behave import given, when, then

@when('I perform custom action')
def step_custom_action(context):
    context.actions.click('#my-element')
    # Use context.actions for Playwright operations
    # Use context.page for direct Playwright access
```

## Using Data Providers

### Excel Data

```python
from framework.data_providers import ExcelProvider

excel = ExcelProvider('test_data/excel/data.xlsx')
data = excel.get_data(sheet='Sheet1', row=2)
print(data['username'])
```

### JSON Data

```python
from framework.data_providers import JsonProvider

json_data = JsonProvider('test_data/json/users.json')
user = json_data.get_by_key_value('id', 1)
print(user['email'])
```

### CSV Data

```python
from framework.data_providers import CsvProvider

csv = CsvProvider('test_data/csv/test_data.csv')
all_data = csv.get_all_data()
for row in all_data:
    print(row['username'])
```

### SQL Data

```python
from framework.data_providers import SqliteProvider, SqlServerProvider

# SQLite
sqlite = SqliteProvider('test_data/database/test.db')
users = sqlite.get_data('SELECT * FROM users WHERE active = ?', (True,))

# SQL Server
sql_server = SqlServerProvider(
    server='localhost',
    database='testdb',
    username='user',
    password='pass'
)
data = sql_server.get_all_data('users')
```

## Using Utilities

### Date Functions

```python
from framework.utils import DateUtils

date_utils = DateUtils()

# Get past date
past_date = date_utils.get_past_date(days=7, format_string='%Y-%m-%d')

# Get future date
future_date = date_utils.get_future_date(months=1, format_string='%Y-%m-%d')

# Compare dates
is_greater = date_utils.is_date_greater('2024-12-31', '2024-01-01')

# Get difference
diff_days = date_utils.get_date_difference('2024-12-31', '2024-01-01', unit='days')
```

### OCR (Text from Images)

```python
from framework.utils import OCRUtils

ocr = OCRUtils()

# Extract text
text = ocr.extract_text('screenshots/image.png')

# Find text location
location = ocr.find_text_location('screenshots/image.png', 'Login')
if location:
    print(f"Text found at: {location['x']}, {location['y']}")

# Verify text presence
has_text = ocr.verify_text_present('screenshots/image.png', 'Welcome')
```

### Image Comparison

```python
from framework.utils import ImageUtils

img_utils = ImageUtils()

# Compare two images
result = img_utils.compare_images('expected.png', 'actual.png', threshold=0.95)
print(f"Similarity: {result['similarity']}, Match: {result['match']}")

# Find image in image
location = img_utils.find_image_in_image('screenshot.png', 'button.png')
if location:
    print(f"Found at: {location['x']}, {location['y']}")

# Highlight differences
diff_image = img_utils.highlight_differences('expected.png', 'actual.png')
```

## Jira Integration

### Configuration

In `config/config.ini`:

```ini
[jira]
enabled = true
server = https://your-domain.atlassian.net
email = your-email@example.com
api_token = ${JIRA_TOKEN}
project_key = PROJ
```

### Usage

Tag scenarios with test case IDs:

```gherkin
@TC-123
Scenario: My test
  ...
```

The framework will automatically create/update Jira issues.

## Zephyr Scale Integration

### Configuration

In `config/config.ini`:

```ini
[zephyr]
enabled = true
api_token = ${ZEPHYR_TOKEN}
test_cycle_key = PROJ-C123
```

### Usage

Test results are automatically pushed to Zephyr Scale after execution.

## Reporting

### HTML Report

Generated automatically in `reports/` directory after test execution.

### Allure Report

```bash
# Run tests with Allure formatter
behave -f allure_behave.formatter:AllureFormatter -o allure-results

# Generate and view report
allure serve allure-results
```

### Email Report

Configure in `config/config.ini`:

```ini
[email]
enabled = true
smtp_server = smtp.gmail.com
smtp_port = 587
from_email = automation@example.com
to_emails = team@example.com,manager@example.com
```

Reports are sent automatically after test execution.

## CI/CD Integration

### GitHub Actions

Create `.github/workflows/tests.yml`:

```yaml
name: Run Tests

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
      
      - name: Run tests
        run: python run_tests.py --tags smoke --headless
        env:
          JIRA_TOKEN: ${{ secrets.JIRA_TOKEN }}
          ZEPHYR_TOKEN: ${{ secrets.ZEPHYR_TOKEN }}
      
      - name: Upload screenshots
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: screenshots
          path: screenshots/
```

## Best Practices

1. **Use Tags**: Organize tests with tags for easy filtering
2. **Page Objects**: Create page object classes for complex pages
3. **Data-Driven**: Use data providers for parameterized tests
4. **Reusable Steps**: Leverage existing step definitions
5. **Clear Naming**: Use descriptive scenario and step names
6. **Proper Waits**: Use explicit waits instead of sleep
7. **Clean Up**: Use Background/hooks for setup and teardown
8. **Screenshots**: Take screenshots for debugging
9. **Logging**: Add informative log messages
10. **Version Control**: Keep test data and configs in version control

## Troubleshooting

### Playwright browsers not found

```bash
playwright install
```

### Tesseract not found (for OCR)

Ubuntu/Debian:
```bash
sudo apt-get install tesseract-ocr
```

macOS:
```bash
brew install tesseract
```

Windows:
Download from https://github.com/UB-Mannheim/tesseract/wiki

### Database connection issues

- Verify connection strings in config
- Ensure database drivers are installed
- Check firewall/network settings

### Jira/Zephyr connection fails

- Verify API tokens are correct
- Check server URLs
- Ensure proper permissions

## Support

For issues and questions:
- Check documentation in `docs/` directory
- Review example tests in `features/`
- Consult the README.md

## Next Steps

- Explore the framework structure
- Review the example feature file
- Create your first test
- Configure integrations
- Set up CI/CD pipeline
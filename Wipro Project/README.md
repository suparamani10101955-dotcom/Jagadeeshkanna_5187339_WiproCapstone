# 99acres Selenium Pytest POM Framework

Production-oriented Selenium automation framework for the 99acres website using Python, Selenium WebDriver, Pytest, Allure Reports, and the Page Object Model design pattern.

## Project Structure

```text
.
├── config/                 # Configuration and environment settings
├── logs/                   # Runtime log files
├── pages/                  # Page Object Model classes
├── reports/                # Allure results and generated reports
├── screenshots/            # Screenshots captured on test failure
├── tests/                  # Pytest test scripts
├── utilities/              # Reusable browser, logging, screenshot utilities
├── conftest.py             # Pytest fixtures and hooks
├── pytest.ini              # Pytest configuration and markers
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create a local `.env` file:

```powershell
Copy-Item .env.example .env
```

4. Optional login data:

```text
ACRES_USERNAME=your_mobile_or_email
ACRES_PASSWORD=your_password_if_applicable
```

99acres often uses OTP-based login. Credential-based login tests skip automatically unless `ACRES_USERNAME` is configured.

## Execute Tests

Run the full suite:

```powershell
pytest
```

Run smoke tests:

```powershell
pytest -m smoke
```

Run a specific suite:

```powershell
pytest -m login
pytest -m search
pytest -m navigation
pytest -m e2e
```

Run the complete single-browser end-to-end workflow:

```powershell
pytest -m e2e -v -s
```

The `driver` fixture is session-scoped, so Chrome is launched once and closed only after the pytest session finishes.

Run with custom browser/base URL options:

```powershell
pytest --browser edge --base-url https://www.99acres.com/
```

Run headless:

```powershell
pytest --headless
```

## Test Data

All reusable test input values are managed in `test_data/test_data.xml`, an Excel 2003 XML workbook that opens directly in Excel.
Each worksheet maps to a test-data section such as `login`, `navigation`, or `property_search`.

Every worksheet uses the same three columns:

- `key`
- `value`
- `type`

Supported `type` values are `str`, `int`, `float`, `bool`, `list`, and `json`.
Use `list` for JSON arrays such as navigation menus or future filter sets.

Credential values can also be supplied through `.env` using `ACRES_USERNAME` and `ACRES_PASSWORD`.
Environment values override the Excel login values at runtime so real credentials can stay outside source control.

Run with a different test data workbook:

```powershell
pytest --test-data test_data/test_data.xml
```

## Allure Reports

Generate Allure results while executing tests:

```powershell
pytest --alluredir=allure-results
```

Generate the HTML report:

```powershell
allure generate allure-results -o reports/allure-report --clean
```

Open the report:

```powershell
allure open reports/allure-report
```

The Allure command-line tool must be installed separately and available on `PATH`.

## Framework Features

- Page Object Model with reusable page classes.
- Centralized Selenium driver creation for Chrome.
- Pytest fixtures for browser setup and teardown.
- Pytest hook for automatic screenshot capture on failed tests.
- Allure attachments for screenshots and failed-test URLs.
- Configurable environment values through `.env`.
- Centralized Excel-backed test data loaded through a reusable pytest fixture.
- Python logging to both console and timestamped log files.
- Assertions and exception handling in page utilities and tests.

## Notes for Maintenance

- Keep selectors inside page classes only.
- Avoid hard-coded credentials in tests.
- Add new page interactions as page methods, not inline Selenium calls in tests.
- Keep tests focused on business behavior and assertions.

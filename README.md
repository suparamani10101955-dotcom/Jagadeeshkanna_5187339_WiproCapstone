# 99acres Behave Automation

## Structure

- `features/test_e2e_99acres.feature`
- `features/login.feature` 
- `features/search.feature`
- `features/filters.feature`
- `features/property_details.feature`
- `features/environment.py`
- `features/steps/e2e_steps.py`
- `features/steps/login_steps.py`
- `features/steps/search_steps.py`
- `features/steps/filter_steps.py`
- `features/steps/property_steps.py`
- `pages/login_page.py`
- `utils/driver_factory.py`
- `utils/wait_utils.py`
- `utils/logger.py`
- `utils/screenshot.py`
- `requirements.txt`

## Reports

- `reports/allure-results/`
- `reports/allure-report/`
- `reports/screenshots/`
- `reports/logs/`

## Setup

```bash
pip install -r requirements.txt
```

## Run

```bash
behave
```

## Run Only E2E

```bash
behave features/test_e2e_99acres.feature
```

## Run Only Individual Login Test

```bash
behave features/login.feature
```

## Run With Allure Formatter

```bash
behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results ./features
```

## Serve Allure Report

```bash
allure serve reports/allure-results
```

## Notes

- The login flow pauses for manual OTP entry using `input(...)`.
- If standard input is unavailable, it falls back to `time.sleep(30)`.
- ChromeDriver is handled through `webdriver-manager`.
- Failure screenshots are captured automatically at step and scenario level.
- Logs are written to `reports/logs/automation.log`.

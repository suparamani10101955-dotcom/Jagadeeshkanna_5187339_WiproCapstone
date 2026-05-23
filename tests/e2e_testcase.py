import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_FILE = PROJECT_ROOT / "features" / "test_e2e_99acres.feature"
ALLURE_REPORT = PROJECT_ROOT / "reports" / "allure-report"


if __name__ == "__main__":
    result = subprocess.run(
        [sys.executable, "-m", "behave", str(FEATURE_FILE)],
        cwd=PROJECT_ROOT,
        check=False,
    )
    if result.returncode == 0:
        try:
            subprocess.run(
                [
                    "allure",
                    "generate",
                    str(PROJECT_ROOT / "reports" / "allure-results"),
                    "--clean",
                    "-o",
                    str(ALLURE_REPORT),
                ],
                cwd=PROJECT_ROOT,
                check=False,
            )
        except FileNotFoundError:
            print("Allure CLI was not found in PATH. Test execution passed, but report generation was skipped.")
    sys.exit(result.returncode)

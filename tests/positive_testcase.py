import subprocess
import sys
from pathlib import Path
import shutil


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FEATURE_FILE = PROJECT_ROOT / "features" / "positive_testcase.feature"
ALLURE_RESULTS = PROJECT_ROOT / "reports" / "allure-results"
ALLURE_REPORT = PROJECT_ROOT / "reports" / "allure-report"


if __name__ == "__main__":
    if ALLURE_RESULTS.exists():
        shutil.rmtree(ALLURE_RESULTS)
    ALLURE_RESULTS.mkdir(parents=True, exist_ok=True)
    result = subprocess.run([sys.executable, "-m", "behave", str(FEATURE_FILE)], cwd=PROJECT_ROOT, check=False)
    if result.returncode == 0:
        subprocess.run(
            [
                "allure",
                "generate",
                str(ALLURE_RESULTS),
                "--clean",
                "-o",
                str(ALLURE_REPORT),
            ],
            cwd=PROJECT_ROOT,
            check=False,
        )
    sys.exit(result.returncode)

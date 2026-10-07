from pathlib import Path
import sys


class AppConfig:
    WINDOW_TITLE = "Мини-автосалон"
    WINDOW_WIDTH = 750
    WINDOW_HEIGHT = 600

    if getattr(sys, "frozen", False):
        BASE_DIR = Path(sys.executable).resolve().parent
    else:
        BASE_DIR = Path(__file__).resolve().parent

    REPORT_PATH = BASE_DIR / "report.txt"
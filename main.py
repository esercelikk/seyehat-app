"""
Compatibility launcher for the SEYEHAT app.

The application source files live under "kaynak kodları". Keeping this file at
the project root lets existing shortcuts and `python main.py` keep working.
"""

from __future__ import annotations

import runpy
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent
SOURCE_DIR = ROOT_DIR / "kaynak kodları"
ENTRYPOINT = SOURCE_DIR / "main.py"

if not ENTRYPOINT.exists():
    raise FileNotFoundError(f"Application entrypoint not found: {ENTRYPOINT}")

source_dir_text = str(SOURCE_DIR)
if source_dir_text not in sys.path:
    sys.path.insert(0, source_dir_text)

runpy.run_path(str(ENTRYPOINT), run_name="__main__")

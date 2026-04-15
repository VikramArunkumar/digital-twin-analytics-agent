from __future__ import annotations

import os

APP_NAME = "digital_twin_ai_starter"
DEFAULT_MODEL = os.getenv("DT_MODEL", "stub-gpt")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

config_file = Path.home() / ".makima" / "config.json"
config = {}
if config_file.exists():
    with open(config_file, "r") as f:
        config = json.load(f)

GROQ_API_KEY = config.get("groq_api_key") or os.getenv("GROQ_API_KEY")
MODEL_NAME = config.get("model") or "qwen/qwen3.6-27b"
TOKEN_LIMIT = 6000
PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
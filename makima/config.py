# import os
# import sys
# from makima.setup import setup_api_key,setup_model
# from dotenv import load_dotenv
# load_dotenv()

# GROQ_API_KEY = setup_api_key()
# # GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# MODEL_NAME = setup_model()
# TOKEN_LIMIT = 10000
# # PROJECT_ROOT = os.getcwd()
# PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

# if not GROQ_API_KEY:
#     print("Error: GROQ_API_KEY not set.")
#     print("Run this command first:")
#     print('  Windows: setx GROQ_API_KEY "your-key-here"')
#     print('  Linux/Mac: export GROQ_API_KEY="your-key-here"')
#     print("Get a free key at: https://console.groq.com")
#     sys.exit(1)

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
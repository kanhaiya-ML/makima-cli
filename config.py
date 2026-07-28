import os
import sys
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3.6-27b"
TOKEN_LIMIT = 10000
# PROJECT_ROOT = os.getcwd()
PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set in .env file")
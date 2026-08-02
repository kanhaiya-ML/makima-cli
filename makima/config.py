import os
import sys
from makima.setup import setup_api_key,setup_model
from dotenv import load_dotenv
load_dotenv()

GROQ_API_KEY = setup_api_key()
# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = setup_model()
TOKEN_LIMIT = 10000
# PROJECT_ROOT = os.getcwd()
PROJECT_ROOT = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY not set.")
    print("Run this command first:")
    print('  Windows: setx GROQ_API_KEY "your-key-here"')
    print('  Linux/Mac: export GROQ_API_KEY="your-key-here"')
    print("Get a free key at: https://console.groq.com")
    sys.exit(1) 
from groq import Groq
from makima.providers.base import LLMProvider
from makima.config import MODEL_NAME
import os
import json
from pathlib import Path

class GroqProvider(LLMProvider):

    def __init__(self):
        # read fresh from config file
        key = self._load_key()
        self.client = Groq(api_key=key)

    def _load_key(self):
        config_file = Path.home() / ".makima" / "config.json"
        if config_file.exists():
            with open(config_file, "r") as f:
                data = json.load(f)
                key = data.get("groq_api_key")
                if key:
                    return key
        return os.getenv("GROQ_API_KEY")

    def chat(self, messages: list, tools: list) -> object:
        return self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            max_tokens=1024
        )

    def stream_chat(self, messages: list, tools: list):
        return self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            max_tokens=1024,
            stream=True
        )
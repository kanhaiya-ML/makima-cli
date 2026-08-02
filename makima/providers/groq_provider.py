from groq import Groq
from makima.providers.base import LLMProvider
from makima.config import GROQ_API_KEY, MODEL_NAME

class GroqProvider(LLMProvider):

    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)

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
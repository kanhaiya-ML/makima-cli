class Memory:

    def __init__(self, system_prompt: str):
        self.messages = [{"role": "system", "content": system_prompt}]

    def add_user(self, text: str):
        self.messages.append({"role": "user", "content": text})

    def add_assistant(self, text: str):
        self.messages.append({"role": "assistant", "content": text})

    def add_tool_result(self, tool_call_id: str, content: str):
        self.messages.append({
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": content
        })

    def add_raw(self, message):
        self.messages.append(message)

    def get(self) -> list:
        return self.messages
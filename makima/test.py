from textual.app import App
from textual.widgets import Header, Footer, Input, RichLog
from rich.text import Text

from makima.providers.groq_provider import GroqProvider
from makima.core.memory import Memory

SYSTEM_PROMPT = "..."
class Makima(App):

    def on_mount(self):
        self.provider = GroqProvider()
        self.memory = Memory(system_prompt=SYSTEM_PROMPT)

    def compose(self):
        yield Header()

        yield RichLog(id="chat")

        yield Input(
            placeholder="Ask Makima...",
            id="input"
        )

        yield Footer()

    def on_input_submitted(self, event: Input.Submitted):
        chat = self.query_one("#chat", RichLog)

        user_input = event.value.strip()

        if not user_input:
            return

        chat.write(
            Text(f"You: {user_input}",style="bold cyan")
        )
        

        event.input.value = ""

        chat.write(
            Text("Makima: Hello! I'm alive", style="bold green")
        )
        # chat.write("[bold green]Makima:[/] Hello! I'm alive")

if __name__ == "__main__":
    app = Makima()
    app.run()
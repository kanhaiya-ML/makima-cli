from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog
from makima.config import PROJECT_ROOT
from makima.tools import TOOL_REGISTRY
from makima.tools.registry import TOOL_SCHEMAS
from makima.core.config_manager import handle_config, analyze_changes, commit_only
from makima.tools.git_tools import commit_and_push

import asyncio
import json

from makima.providers.groq_provider import GroqProvider
from makima.core.memory import Memory

from pathlib import Path


SYSTEM_PROMPT = f"""
You are a coding assistant. The project is at: {PROJECT_ROOT}

Rules:
- Always use list_files first to find exact paths
- Always use read_file before editing any file
- Use full absolute paths always
- Be concise and direct
- old_str must be an exact match of multiple lines from the file
- Never explain what you are about to do. Never say "Let me..." or "I'll first...".
- Just call the tool immediately and silently.
- Only speak in plain text when you have a FINAL answer for the user.
- Call only ONE tool per response. Wait for the tool result before calling the next tool.
- Never output multiple tool calls in one response.
"""


class MakimaApp(App):
    CSS_PATH = Path(__file__).parent / "app.tcss"
    
    def __init__(self):
        super().__init__()
        self.memory = Memory(system_prompt=SYSTEM_PROMPT)
        self.provider = GroqProvider()
        self.pending_commit = None

    
    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="chat",markup=True, highlight=True)
        yield Input(placeholder="Ask anything... (type 'exit' to quit)")
        yield Footer()
    
    def on_mount(self):
        # focus the input so user can type immediately
        self.query_one(Input).focus()


    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_input = event.value.strip()

        if not user_input:
            return

        chat = self.query_one(RichLog)
        input_box = self.query_one(Input)

        chat.write(f"[bold blue]You:[/] {user_input}")
        input_box.clear()

        if user_input == "exit":
            self.exit()
            return

        if user_input == "/config":
            # config runs in background thread
            await asyncio.to_thread(handle_config)
            return

        if user_input == "/commit":
            chat.write("[dim]Analyzing changes...[/]")
            diff, message = await asyncio.to_thread(analyze_changes)

            if not diff:
                chat.write("[yellow]No changes to commit.[/]")
                return

            chat.write(f"[white]Generated message: {message}[/]")
            chat.write("[yellow]Type 'push' to commit and push, 'commit' to commit only, or 'cancel'[/]")

            self.pending_commit = {"diff": diff, "message": message}
            return

        if user_input == "push" and self.pending_commit:
            result = await asyncio.to_thread(commit_and_push, self.pending_commit["message"])
            chat.write(f"[green]{result}[/]")
            self.pending_commit = None
            return

        if user_input == "commit" and self.pending_commit:
            result = await asyncio.to_thread(commit_only, self.pending_commit["message"])
            chat.write(f"[green]{result}[/]")
            self.pending_commit = None
            return

        if user_input == "cancel" and self.pending_commit:
            chat.write("[yellow]Commit cancelled.[/]")
            self.pending_commit = None
            return
        
        
        # show thinking indicator
        chat.write("[dim]thinking...[/]")
        
        # run agent in background thread
        response = await asyncio.to_thread(self.process_message, user_input)
        
        # remove "thinking..." and show response
        from rich.markdown import Markdown
        chat.write(Markdown(f"[bold green]Agent:[/] {response}"))


    def process_message(self, user_input):
        self.memory.add_user(user_input)
        
        while True:
            stream = self.provider.stream_chat(
                messages=self.memory.get(),
                tools=TOOL_SCHEMAS
            )
            chunks = list(stream)
            
            # collect chunks
            text_buffer = ""
            tool_name = ""
            tool_args = ""
            tool_call_id = ""
            is_tool_call = False
            
            for chunk in chunks:
                delta = chunk.choices[0].delta
                if delta.content:
                    text_buffer += delta.content
                if delta.tool_calls:
                    is_tool_call = True
                    tc = delta.tool_calls[0]
                    if tc.id:
                        tool_call_id = tc.id
                    if tc.function.name:
                        tool_name += tc.function.name
                    if tc.function.arguments:
                        tool_args += tc.function.arguments
            
            if is_tool_call:
                args = json.loads(tool_args)
                tool_fn = TOOL_REGISTRY.get(tool_name)
                result = tool_fn(**args) if tool_fn else "Unknown tool"
                
                self.memory.add_raw({
                    "role": "assistant",
                    "tool_calls": [{
                        "id": tool_call_id,
                        "type": "function",
                        "function": {
                            "name": tool_name,
                            "arguments": tool_args
                        }
                    }]
                })
                self.memory.add_tool_result(tool_call_id, str(result))
            
            else:
                self.memory.add_assistant(text_buffer)
                return text_buffer
def run_ui():
    app = MakimaApp()
    app.run()
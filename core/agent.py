import json
from config import PROJECT_ROOT,MODEL_NAME
from core.context import ContextManager
from core.memory import Memory
from tools import TOOL_REGISTRY
from tools.registry import TOOL_SCHEMAS
from providers.groq_provider import GroqProvider
from rich.console import Console


console = Console()

ctx = ContextManager()
context = ctx.build_context()

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

import pyfiglet
from rich.panel import Panel
from rich.text import Text
from rich.rule import Rule
from rich.markdown import Markdown


def run_agent():
    provider = GroqProvider()
    memory = Memory(system_prompt=SYSTEM_PROMPT)


    ascii_art = pyfiglet.figlet_format("Makima", font="big")
    console.print(f"[bold #FF6B35]{ascii_art}[/]")

    # info line underneath, no box
    console.print(f"[dim]  Your AI Coding Assistant[/]")
    console.print(f"[green]  Project :[/] {PROJECT_ROOT}")
    console.print(f"[green]  Files   :[/] {len(ctx.files)} files loaded")
    console.print(f"[green]  Model   :[/] {MODEL_NAME}")
    console.print(f"[dim]  Type 'exit' to quit[/]")
    console.print(Rule(style="#FF6B35"))  # clean horizontal line separator
    console.print()

    while True:
        user_input = console.input("[bold blue]You:[/] ")
        if user_input.strip() == "exit":
            break

        memory.add_user(user_input)

        while True:
            try:
                with console.status("[yellow]thinking...[/]"):
                    stream = provider.stream_chat(
                        messages=memory.get(),
                        tools=TOOL_SCHEMAS
                    )
                    chunks = list(stream)
            except Exception as e:
                console.print(f"[red]Error: {e}[/]")
                break

            #variables to collect the response
            text_buffer = ""
            tool_name = ""
            tool_args = ""
            tool_call_id = ""
            is_tool_call = False

            # console.print("[bold green]Agent:[/] ", end="")

            
            for chunk in chunks:
                delta = chunk.choices[0].delta

                #text chunk
                if delta.content:
                    # print(delta.content, end="", flush=True)
                    text_buffer += delta.content


                # tool call chunk
                if delta.tool_calls:
                    is_tool_call = True
                    tc = delta.tool_calls[0]
                    if tc.id:
                        tool_call_id = tc.id
                    if tc.function.name:
                        tool_name += tc.function.name
                    if tc.function.arguments:
                        tool_args += tc.function.arguments

            # print()

            if is_tool_call:
                console.print(f"[dim]⚡ {tool_name}[/]")

                with console.status(f"[yellow]calling {tool_name}...[/]"):
                    args = json.loads(tool_args)
                    tool_fn = TOOL_REGISTRY.get(tool_name)
                    result = tool_fn(**args) if tool_fn else "Unknown tool"

                # build the assistant message manually for memory
                memory.add_raw({
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
                memory.add_tool_result(tool_call_id, str(result))

            else:
                console.print("[bold green]Agent:[/]")
                console.print(Markdown(text_buffer))
                memory.add_assistant(text_buffer)
                break
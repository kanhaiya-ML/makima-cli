from pathlib import Path
from groq import Groq
import json
from rich.console import Console
console = Console()


def validate_key(key):
    try:
        client = Groq(api_key=key)
        client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[{"role": "user", "content": "say hi"}],
            max_tokens=5
        )
        return True
    except:
        return False

    
def setup_api_key():

    config_dir = Path.home() / ".makima"
    config_file = config_dir / "config.json" 

    if config_file.exists():
        with open(config_file, "r") as f:
            data = json.load(f)
            key = data["groq_api_key"]
            return key

    import os
    env_key = os.getenv("GROQ_API_KEY")
    if env_key:
        return env_key

    console.print("[bold]Welcome to Makima CLI![/]")
    console.print("[dim]Get a free key at https://console.groq.com[/]\n")

    while True:
        key = console.input("[bold yellow]Enter your Groq API key:[/] ").strip()
        
        with console.status("[yellow]Authenticating...[/]"):
            valid = validate_key(key)
        
        if valid:
            console.print("[bold green]✓ Connected to Groq[/]")
            config_dir.mkdir(exist_ok=True)
            with open(config_file, "w") as f:
                json.dump({"groq_api_key": key}, f)
            return key
        else:
            console.print("[bold red]✗ Invalid key. Try again.[/]")
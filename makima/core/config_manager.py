from pathlib import Path
import json
from makima.setup import validate_key
import questionary
from rich.console import Console
console = Console()


def show_config():
    config_dir = Path.home() / ".makima"
    config_file = config_dir / "config.json" 

    try:
        with open(config_file,"r") as f:
            data = json.load(f)
            model = data.get("model")
            key = data.get("groq_api_key")
            console.print("Current setting:")
            console.print(f"Model: {model}")
            console.print(f"Key: {key[:8]}****")
            # console.print("What do you want to change?")
            # options = questionary.select(
            #     "What do you want to change?",
            #     choices = [
            #         "Change Model",
            #         "Change API key",
            #         "Cancel"
            #     ]
            # )

    except Exception as e:
        return f"Somthing went wrong! {e}"


def change_model():
    config_dir = Path.home() / ".makima"
    config_file = config_dir / "config.json" 

    if config_file.exists():
        with open(config_file,"r") as f:
            data = json.load(f)
            model = data.get("model")
            if model:
                console.print(f"Selected Model: {model}")

    model = questionary.select(
        "Select a model: ",
        choices = [
            "llama-3.3-70b",
            "qwen/qwen3.6-27b", 
            "gemma2-9b"
        ]
    ).ask()


    existing = {}
    if config_file.exists():
        with open(config_file,"r") as f:
            existing = json.load(f)

    existing["model"] = model

    with open(config_file,"w") as f:
        json.dump(existing,f)

    console.print(f"[bold green]✓ Model changed to: {model}[/]")
    return model

    # if model:
    #     console.print(f"[bold green]✓ Model Selected: {model} [/]")
    #     config_dir.mkdir(exist_ok=True)
    #     with open(config_file,"w") as f:
    #         json.dump({"model":model}, f)
    #     return model
    # else:
    #     console.print("[bold red]✗ Please Select in Given models.[/]")



def change_api_key():
    config_dir = Path.home() / ".makima"
    config_file = config_dir / "config.json" 

    if config_file.exists():
        with open(config_file,"r") as f:
            data = json.load(f)
            key = data.get("groq_api_key")
            if key:
                console.print(f"Already Setted API key: {key}")

    while True:

        key = console.input("[bold yellow]Enter your Groq API key:[/] ").strip()

        with console.status("[yellow]Authenticating...[/]"):
            valid = validate_key(key)

            if valid:
                console.print("[bold green]✓ Connected to Groq[/]")
                config_dir.mkdir(exist_ok=True)
                existing = {}
                if config_file.exists():
                    with open(config_file, "r") as f:
                        existing = json.load(f)
                existing["groq_api_key"] = key
                with open(config_file, "w") as f:
                    json.dump(existing, f)
                return key
            else:
                console.print("[bold red]✗ Invalid key. Try again.[/]")



def handle_config():
    show_config()

    choice = questionary.select(
        "What do you want to change?",
        choices=["Change model", "Change API key", "Cancel"]
    ).ask()

    if choice == "Change model":
        change_model()
    elif choice == "Change API key":
        change_api_key()


from makima.tools.git_tools import get_git_diff, generate_commit_message, commit_and_push
import subprocess
import os

def commit_only(message):
    cmd = f'git add -A && git commit -m "{message}"'
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        return "✓ Committed locally"
    return f"✗ Failed: {result.stderr}"


def analyze_changes():
    diff = get_git_diff()

    if not diff.strip():
        return None, None
    message = generate_commit_message(diff)
    return  diff, message


def handle_commit():
    diff = get_git_diff()

    if not diff.strip():
        console.print("[yellow]No changes to commit.[/]")
        return
    
    commit_message = generate_commit_message(diff=diff)
    console.print(f"[white] {commit_message}")

    # choice = questionary.select(
    #     "What action you want?: ",
    #     choices = [
    #         "commit_and_push",
    #         "commit only",
    #         "cancle"
    #     ]
    # ).ask()

    # if choice == "commit_and_push":
    #     result = commit_and_push(message=commit_message)
    #     console.print(f"[green]{result}[/]")
    # elif choice == "commit only":
    #     result = commit_only(diff)
    #     console.print(f"[green]{result}[/]")

        

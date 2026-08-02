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
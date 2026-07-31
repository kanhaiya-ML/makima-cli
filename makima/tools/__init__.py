from makima.tools.file_tools import read_file, list_files, edit_file, create_file
from makima.tools.shell_tools import run_command

TOOL_REGISTRY = {
    "read_file": read_file,
    "list_files": list_files,
    "edit_file": edit_file,
    "run_command": run_command,
    "create_file": create_file,
}
import subprocess


def run_command(cmd):
    # print(f"Commands going to Run: {cmd}")
    # User_answer = input("Run This? (Y/N): ")
    # User_answer = User_answer.lower()

    # if User_answer != "y":
    #     return "Command cancelled"

    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
        timeout=30
    )

    return result.stdout + result.stderr
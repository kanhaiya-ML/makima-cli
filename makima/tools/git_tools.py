import subprocess
from groq import Groq
from makima.config import GROQ_API_KEY, PROJECT_ROOT
import re


def get_git_diff():
    diff = subprocess.run("git diff", shell=True, text=True, capture_output=True)
    status = subprocess.run("git status", shell=True, text=True, capture_output=True)

    return f"STATUS:\n{status.stdout}\n\nDIFF:\n{diff.stdout}"


def generate_commit_message(diff):

    # prompt = f"""Generate ONE git commit message for this diff.
    #     Format: type(scope): description
    #     Types: feat/fix/refactor/docs/chore
    #     Rules: max 72 chars, no quotes, no backticks, no explanation
    #     Return ONLY the commit message line, nothing else.

    prompt = f"""Generate ONE git commit message for this diff.
    Format: type(scope): description
    Types: feat/fix/refactor/docs/chore
    Rules: max 72 chars, no quotes, no backticks, no explanation
    Return ONLY the commit message line, nothing else.

    {diff[:3000]}"""
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
        result = client.chat.completions.create(
            model="qwen/qwen3.6-27b",
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )
    except Exception as e:
        print(f"Message Generator Failed!\n {e}")
        return f"Failed to generate message: {e}"

    content = result.choices[0].message.content
    if "</think>" in content:
        content = content.split("</think>")[-1].strip()
    content = re.sub(r'[`\n]', '', content).strip()
    return content


def commit_and_push(message):
    try:
        message = clean_message(message)
        cmd = f'git add -A && git commit -m "{message}" && git push origin main'
        result = subprocess.run(
            cmd,
            shell=True,
            text=True,
            capture_output=True,
            timeout=120,
            cwd=PROJECT_ROOT
        )
        if result.returncode == 0:
            return f"✓ Committed and pushed: {message}"
        else:
            return f"✗ Failed: {result.stderr}"
    except Exception as e:
        return f"✗ Error: {e}"



def clean_message(message):
    # remove thinking blocks
    if "</think>" in message:
        message = message.split("</think>")[-1].strip()
    # remove backticks, quotes, special shell characters
    message = re.sub(r'[`"\'\n]', '', message)
    # remove any remaining markdown
    message = message.strip()
    return message
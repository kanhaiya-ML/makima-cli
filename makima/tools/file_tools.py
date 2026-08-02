from makima.config import PROJECT_ROOT
import os
import git

def read_file(path):
    if not os.path.exists(path):
        path = os.path.join(PROJECT_ROOT, path)
    try:
        with open(path, "r") as content:
            return content.read()
    except Exception as e:
        return f"There is an Error while Reading your files. Error - {e}"


def list_files():
    skip = {"__pycache__", ".git", "node_modules", ".env",".venv"}
    output = []

    for folder, subfolders, files in os.walk(PROJECT_ROOT):

        subfolders[:] = [f for f in subfolders if f not in skip]

        output.append(folder)
        for file in files:
            output.append(" " + file)

    return "\n".join(output)


def edit_file(path, old_str, new_str):
    auto_commit(path)
    
    if not os.path.exists(path):
        path = os.path.join(PROJECT_ROOT,path)
        
    readed_content = read_file(path)
    if old_str in readed_content:
        new_contents = readed_content.replace(old_str,new_str,1)
    else:
        return f"content that i tried to change is missing"

    with open(path,"w") as f:
        f.write(new_contents)
    return f"Done. Edited {path}"



def create_file(path, content):
    if os.path.exists(path):
        return f"File already exists: {path}"

    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        f.write(content)
    return f"Created path: {path}"


def auto_commit(path):
    try:
        repo = git.Repo(PROJECT_ROOT)
        repo.git.add(path)
        repo.index.commit(f"auto-backup before edit: {path}")
    except Exception as e:
        pass
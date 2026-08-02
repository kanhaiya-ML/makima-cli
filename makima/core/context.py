from makima.config import PROJECT_ROOT,TOKEN_LIMIT
from makima.tools.file_tools import read_file,list_files
import os


class ContextManager:
    def __init__(self):
        self.files = []
        self.total_tokens = 0
        self.scan_files()


    def scan_files(self):
        skip = {"__pycache__", ".git", "node_modules", ".env",".venv"}
        skip_ext = {".pyc", ".png", ".jpg", ".jpeg", ".gif", ".ico"}
        self.files = []

        for folder, subfolders, files in os.walk(PROJECT_ROOT):
            subfolders[:] = [f for f in subfolders if f not in skip]

            for file in files:

                if any(file.endswith(ext) for ext in skip_ext):
                    continue
                file_path = os.path.join(folder,file)
                self.files.append(file_path)


    def count_tokens(self,text):
        return len(text) // 4


    def build_context(self):

        context = ""

        for file in self.files:
            content = read_file(file)

            self.total_tokens += self.count_tokens(content)

            if self.total_tokens > TOKEN_LIMIT:
                return "TOO LARGE CONTEXT"
            else:
                context += f"\n--- {file} ---\n{content}\n"

        return context
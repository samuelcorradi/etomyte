from pathlib import Path
from etomyte.core.cms import AdapterBase
from git_repo.src.etomyte.core.server import App

class FileAdapter(AdapterBase):
    def __init__(self, app:App):
        self.app = app
        base_path = Path(app.config.get("BASE_PATH", ".")).resolve()
        self.base_path = base_path

    def __read_file(self, path:str)->str:
        """
        Look for base_dir / rel_path + ext for each ext in order.
        """
        candidate = self.base_path / (path.strip("/"))
        ext = '.md'
        filepath = candidate.with_suffix(ext)
        print(f"Looking for file: {filepath}")
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def get_content(self, path:str)->str:
        """
        Retrieve content for the given path.
        """
        path = path.strip("/") or "index"
        path = Path("contents") / path.lstrip("/")
        return self.__read_file(str(path))

    def get_template(self, path:str)->str:
        """
        Implement file-based template retrieval.
        """
        path = path.strip("/") \
            or self.app.config.get("DEFAULT_TEMPLATE", "index")
        path = Path("templates") / path.lstrip("/")
        return self.__read_file(str(path))
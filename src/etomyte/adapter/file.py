from pathlib import Path
from etomyte.core.cms import AdapterBase

class FileAdapter(AdapterBase):
    def __init__(self, home:str):
        base_path = Path(home).resolve()
        self.base_path = base_path

    def __read_file(self, path:str)->str:
        """
        Look for base_dir / rel_path + ext for each ext in order.
        """
        candidate = self.base_path / (path.strip("/"))
        try:
            with open(candidate, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None

    def get_snippet(self, name:str)->str:
        """
        Retrieve snippet code for the given name.
        """
        ext = '.py'
        path = Path("snippets") / (name.strip("/").split("/")[0])
        filepath = path.with_suffix(ext)
        return self.__read_file(str(filepath))

    def get_content(self, path:str)->str:
        """
        Retrieve content for the given path.
        """
        ext = '.md'
        path = path.strip("/") or "index"
        path = Path("contents") / path.lstrip("/")
        filepath = path.with_suffix(ext)
        return self.__read_file(str(filepath))

    def get_template(self, path:str)->str:
        """
        Implement file-based template retrieval.
        """
        ext = '.md'
        path = path.strip("/") or "index"
        path = Path("templates") / path.lstrip("/")
        filepath = path.with_suffix(ext)
        return self.__read_file(str(filepath))
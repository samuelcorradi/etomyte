from pathlib import Path
from etomyte.core.cms import AdapterBase

class FileAdapter(AdapterBase):
    def __init__(self, home:str):
        base_path = Path(home).resolve()
        self.base_path = base_path
        self.templates_dir = base_path/"templates"
        self.contents_dir = base_path/"contents"
        self.snippets_dir = base_path/"snippets"

    @staticmethod
    def create_project(name:str)->None:
        """
        """
        base = Path(name)
        dirs = [
            base/"config",
            base/"contents",
            base/"snippets",
            base/"templates",
        ]
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {d}")
        # minimal config files
        config_py = base/"config"/"config.py"
        text = """# project configuration
    HOST = "127.0.0.1"
    PORT = 8000

    # name of the root/default template (without extension)
    DEFAULT_TEMPLATE = "index"
    """
        config_py.write_text(text, encoding="utf-8")
        # routes.py with example route
        routes_py = base/"config"/"routes.py"
        text = """####################################################
    # Define API routes here using the @route decorator
    ####################################################
    from etomyte.core.route import route

    @route("GET", "/hello")
    async def hello():
        return {"message": "hello"}

    @route("POST", "/data")
    async def data():
        return {"ok": True}
    """
        routes_py.write_text(text, encoding="utf-8")
        # default root template
        text = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Etomyte</title>
    </head>
    <body>
        {{content}}
    </body>
    </html>
    """
        (base/"templates"/"index.md").write_text(text, encoding="utf-8")
        # default 404 content
        text = """
    <h1>404 &mdash; Page not found</h1>
    <p>The page you requested could not be found.</p>
    """
        (base/"contents"/"404.md").write_text(text, encoding="utf-8")
        print(f"\nProject '{name}' created successfully.")
        print(f"Run it with: python -m etomyte run \"{base.resolve()}\"")

    def __read_file(self, path:str)->str:
        """
        Look for base_dir / rel_path + ext for each ext in order.
        """
        candidate = Path(path)
        if not candidate.is_absolute():
            candidate = self.base_path/path.strip("/")
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
        path = self.snippets_dir/(name.strip("/").split("/")[0])
        filepath = path.with_suffix(ext)
        return self.__read_file(str(filepath))

    def get_content(self, path:str)->str:
        """
        Retrieve content for the given path.
        """
        ext = '.md'
        path = path.strip("/") or "index"
        path = self.contents_dir / path.lstrip("/")
        filepath = path.with_suffix(ext)
        result = self.__read_file(str(filepath))
        return result

    def get_template(self, path:str)->str:
        """
        Implement file-based template retrieval.
        """
        ext = '.md'
        path = self.templates_dir / path.strip("/")
        filepath = path.with_suffix(ext)
        return self.__read_file(str(filepath))
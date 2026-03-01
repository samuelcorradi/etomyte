import sys
import importlib.util
from pathlib import Path

def create_project(name:str) -> None:
    """
    Create a new Etomyte project directory structure.
    :param name: Name of the project (also the directory name).
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

def _load_config(config_file: Path) -> object:
    """
    Load a Python config module from file path, or return None.
    :param config_file: Path to the config.py file.
    :return: The loaded module object, or None if not found or failed.
    """
    if not config_file.exists():
        return None
    spec = importlib.util.spec_from_file_location("_etomyte_project_config", config_file)
    if spec is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def run_server(project_path:str) -> None:
    """
    Start the Etomyte server for the given project path.
    :param project_path: Path to the Etomyte project directory.
    """
    import uvicorn
    from etomyte import app as app_factory
    app = app_factory(project_path)
    server = app.server
    print(f"Starting Etomyte server  →  http://{server.host}:{server.port}")
    print(f"Project path: {Path(project_path).resolve()}")
    uvicorn.run(app=server.app, host=server.host, port=server.port)

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python -m etomyte <project_name>        Create a new project")
        print("  python -m etomyte run <project_path>    Start the server")
        sys.exit(1)
    if args[0]=="run":
        if len(args) < 2:
            print("Usage: python -m etomyte run <project_path>")
            sys.exit(1)
        run_server(args[1])
    else:
        create_project(args[0])

if __name__ == "__main__":
    main()

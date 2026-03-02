import sys
import importlib.util
from pathlib import Path

def create_project(name:str, adapter_name:str=None) -> None:
    """
    Create a new Etomyte project directory structure.
    :param name: Name of the project (also the directory name).
    :param adapter_name: Optional name of the adapter to use.
    """
    if adapter_name is None:
        adapter_name = "file"
    if adapter_name == "file":
        from etomyte.adapter.file import FileAdapter
        FileAdapter.create_project(name)
    else:
        print(f"Error: Unsupported adapter '{adapter_name}'.")
        sys.exit(1)

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
    from etomyte import app as app_factory
    app = app_factory(project_path)
    server = app.server
    server.run()

def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage:")
        print("  python -m etomyte create <project_name> --path|-p <base_path> [--adapter|-a <adapter_name>]        Create a new project")
        print("  python -m etomyte run <project_path>    Start the server")
        sys.exit(1)
    if args[0]=="run":
        if len(args) < 2:
            print("Usage: python -m etomyte run <project_path>")
            sys.exit(1)
        run_server(args[1])
    elif args[0]=="create":
        if len(args)<2:
            print("Usage: python -m etomyte create <project_name> --path|-p <base_path> [--adapter|-a <adapter_name>]")
            sys.exit(1)
        adapter_name:str = None
        if "--adapter" in args or "-a" in args:
            try:
                adapter_index = args.index("--adapter") if "--adapter" in args else args.index("-a")
                adapter_name = args[adapter_index + 1]
            except IndexError:
                print("Error: Adapter name not provided.")
                adapter_name = None
        create_project(args[1], adapter_name)

if __name__ == "__main__":
    main()

import importlib.util
from pathlib import Path
from fastapi import FastAPI

class Server():
    """
    Servidor para a aplicação Etomyte.
    """
    def __init__(self, port=8000):
        self.port = port
        self.app = FastAPI(title="Etomyte", description="Etomyte CMS server")
        self.__config = {}

    def set_config(self, name:str, value):
        self.__config[name] = value
    
    @property
    def config(self) -> dict:
        return self.__config

    @config.setter
    def config(self, value: dict):
        self.__config = value

    def load_routes(self, routes_path: str) -> None:
        """
        Carrega dinamicamente um ficheiro routes.py
        e aplica as rotas à instância FastAPI.
        O ficheiro deve usar o decorador `@route`
        do Etomyte:
        ```python
        from etomyte.core import route
        @route("GET", "/hello")
        async def hello():
            return {"message": "Hello!"}
        ```
        :param routes_path: Caminho absoluto ou relativo para o ficheiro routes.py.
        :raises FileNotFoundError: Se o ficheiro não existir.
        """
        filepath = Path(routes_path).resolve()
        if not filepath.is_file():
            raise FileNotFoundError(f"Routes file not found: {filepath}")
        
        spec = importlib.util.spec_from_file_location("_etomyte_routes", filepath)
        if spec is None or spec.loader is None:
            raise ImportError(f"Cannot create module spec for: {filepath}")

        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        from etomyte.core.route import get_marked_routes
        marked = get_marked_routes(mod)
        if not marked:
            print(
                f"[etomyte] Warning: {filepath} does not expose any "
                f"@route handlers — no routes were loaded."
            )
            return

        _method_map = {
            "GET": self.app.get,
            "POST": self.app.post,
            "PUT": self.app.put,
            "DELETE": self.app.delete,
            "PATCH": self.app.patch,
            "OPTIONS": self.app.options,
            "HEAD": self.app.head,
        }
        for info, handler in marked:
            method = info["method"]
            path = info["path"]
            registrar = _method_map.get(method)
            if registrar is None:
                self.app.api_route(path, methods=[method])(handler)
            else:
                registrar(path)(handler)

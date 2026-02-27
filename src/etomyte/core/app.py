from pathlib import Path
from fastapi import Request
from typing import Optional
from fastapi.responses import HTMLResponse
from etomyte.core.server import Server
from etomyte.core.cms import CMS
from etomyte.adapter.file import FileAdapter

class Etomyte:
    """
    Classe principal do Etomyte.
    Fornece métodos para configurar o servidor,
    carregar rotas e templates, e executar snippets.
    """
    def __init__(self
        , home:str=None
        , adapter=None
        , default_template:str=None
        , port:int=8000):
        self.home = home
        self.port = port
        self.server = Server(port=port)

        home = Path(home).resolve()
        self.templates_dir = home / "templates"
        self.contents_dir  = home / "contents"
        self.snippets_dir  = home / "snippets"
        config_file = home/"config"/"config.py"
        routes_path = home/"config"/"routes.py"
        if not adapter:
            adapter = FileAdapter(home=home)
        self.cms = CMS(adapter, default_template)
    @staticmethod
    def __load_module(filepath:Path, module_name:str):
        """
        Dynamically load a Python module from a file path.
        """
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            return None
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as exc: # noqa: BLE001
            print(f"[etomyte] Warning: could not load {filepath}: {exc}")
            return None
        return mod

    def load_config(self, config_file:str)->dict:
        # load project config
        if not config_file.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
        config_mod = Etomyte.__load_module(config_file, "_etomyte_config")
        host = getattr(config_mod, "HOST", None)
        port = getattr(config_mod, "PORT", None)
        default_template = getattr(config_mod, "DEFAULT_TEMPLATE", None)
        content_extensions = getattr(config_mod, "CONTENT_EXTENSIONS", None)
        template_extensions = getattr(config_mod, "TEMPLATE_EXTENSIONS", None)
        return {
            "HOST": host,
            "PORT": port,
            "DEFAULT_TEMPLATE": default_template,
            "CONTENT_EXTENSIONS": content_extensions,
            "TEMPLATE_EXTENSIONS": template_extensions
        }

    def __config_route(self):
        # catch-all handler
        @self.server.app.get("/{full_path:path}", response_class=HTMLResponse)
        async def cms_handler(request: Request, full_path: str) -> HTMLResponse:
            request_path = "/" + full_path  # e.g. "/produtos/carros/modeloX"
            # content (exact match)
            content_html = ""
            status_code  = 200
            if self.contents_dir.is_dir():
                content_file = self.cms.get_content(request_path)
                if content_file is None:
                    status_code = 404
                    # try 404 content, fallback to built-in message
                    error_file = self.cms.get_content("/404")
                    if error_file:
                        #content_html = _render_file(error_file)
                        content_html = self.cms.process_snippets(error_file)
                    else:
                        content_html = "<h1>404 &mdash; Page not found</h1>"
                else:
                    # content_html = _render_file(content_file)
                    content_html = self.cms.process_snippets(content_file)
            # template (hierarchical lookup)
            template_html = "{{content}}"
            template_file: Optional[Path] = None
            if self.templates_dir.is_dir():
                template_file = self.cms.get_template(request_path)
                template_html = self.cms.process_snippets(template_file)
            html = template_html.replace("{{content}}", content_html)
            return HTMLResponse(content=html, status_code=status_code)
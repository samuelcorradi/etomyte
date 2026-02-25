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
        self.server.load_routes(routes_path)
        self.__config_route()
        
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
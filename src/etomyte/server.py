"""
Etomyte – FastAPI application factory + CMS engine.
"""
from __future__ import annotations
import importlib.util
import re
from pathlib import Path
from typing import Optional
import markdown
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

# helpers
def _load_module(filepath: Path, module_name: str):
    """Dynamically load a Python module from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    if spec is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(mod)
    except Exception as exc:  # noqa: BLE001
        print(f"[etomyte] Warning: could not load {filepath}: {exc}")
        return None
    return mod

def _render_file(filepath: Path) -> str:
    """Read a file and convert to HTML if Markdown."""
    text = filepath.read_text(encoding="utf-8")
    if filepath.suffix == ".md":
        return markdown.markdown(text, extensions=["fenced_code", "tables"])
    return text

def _find_file(base_dir: Path, rel_path: str, extensions: list[str]) -> Optional[Path]:
    """Look for base_dir / rel_path + ext for each ext in order."""
    for ext in extensions:
        candidate = base_dir / (rel_path.lstrip("/") + ext)
        if candidate.is_file():
            return candidate
    return None

def _find_template(
    templates_dir: Path,
    request_path: str,
    default_name: str,
    extensions: list[str],
) -> Optional[Path]:
    """
    Walk up the path hierarchy to find the closest
    template.
    /produtos/carros/modeloX 
        →  /produtos/carros 
            →  /produtos 
                →  index
    """
    parts = [p for p in request_path.strip("/").split("/") if p]
    while parts:
        rel = "/".join(parts)
        f = _find_file(templates_dir, rel, extensions)
        if f:
            return f
        parts.pop()
    # fallback to default (root) template
    return _find_file(templates_dir, default_name, extensions)

def _find_content(
    contents_dir: Path,
    request_path: str,
    extensions: list[str])->Optional[Path]:
    """
    Exact-match lookup for content files.
    """
    rel = request_path.strip("/") or "index"
    return _find_file(contents_dir, rel, extensions)

def _process_snippets(text: str, snippets_dir: Path) -> str:
    """
    Replace [[snippet_name]] and
    [[snippet_name?key=val,key2=val2]] markers.
    .py snippets must expose a render(params: dict) -> str function.
    .html / .md snippets are rendered as-is (no parameters).
    """
    pattern = re.compile(r"\[\[([^\]]+)\]\]")
    def _replace(match: re.Match)->str:
        full = match.group(1).strip()
        name, snippet_params = full, {}
        if "?" in full:
            name, param_str = full.split("?", 1)
            snippet_params = {
                k: v
                for part in param_str.split(",")
                if "=" in part
                for k, v in [part.split("=", 1)]
            }
        for ext in [".py", ".html", ".md"]:
            candidate = snippets_dir / (name + ext)
            if candidate.is_file():
                if ext == ".py":
                    mod = _load_module(candidate, f"_snippet_{name}")
                    if mod and hasattr(mod, "render"):
                        return str(mod.render(snippet_params))
                    return ""
                return _render_file(candidate)
        # snippet not found – leave marker unchanged so it's visible
        return match.group(0)
    return pattern.sub(_replace, text)

def _build_response(
    template_file: Optional[Path],
    content_html: str,
    snippets_dir: Path) -> str:
    """
    Merge content into template (or return
    content alone).
    """
    if template_file is None:
        return content_html
    template_html = _render_file(template_file)
    template_html = _process_snippets(template_html, snippets_dir)
    return template_html.replace("{{content}}", content_html)

# app factory
def create_app(project_path: str)->FastAPI:
    """
    Create and configure the FastAPI application
    for an Etomyte project.
    :param project_path: Absolute (or relative) path to the Etomyte project directory.
    """
    project_dir = Path(project_path).resolve()
    if not project_dir.is_dir():
        raise FileNotFoundError(f"Project directory not found: {project_dir}")
    templates_dir = project_dir / "templates"
    contents_dir  = project_dir / "contents"
    snippets_dir  = project_dir / "snippets"
    config_file   = project_dir / "config" / "config.py"
    routes_file   = project_dir / "config" / "routes.py"
    # load project config
    config_mod = _load_module(config_file, "_etomyte_config") if config_file.exists() else None
    default_template     = getattr(config_mod, "DEFAULT_TEMPLATE",     "index")
    content_extensions   = getattr(config_mod, "CONTENT_EXTENSIONS",   [".html", ".md"])
    template_extensions  = getattr(config_mod, "TEMPLATE_EXTENSIONS",  [".html", ".md"])
    # FastAPI app
    app = FastAPI(title="Etomyte", description="Etomyte CMS server")
    # custom routes
    if routes_file.exists():
        routes_mod = _load_module(routes_file, "_etomyte_routes")
        if routes_mod:
            if hasattr(routes_mod, "router"):
                app.include_router(routes_mod.router)
            elif hasattr(routes_mod, "setup"):
                routes_mod.setup(app)
    # catch-all handler
    @app.get("/{full_path:path}", response_class=HTMLResponse)
    async def cms_handler(request: Request, full_path: str) -> HTMLResponse:
        request_path = "/" + full_path  # e.g. "/produtos/carros/modeloX"
        # content (exact match)
        content_html = ""
        status_code  = 200
        if contents_dir.is_dir():
            content_file = _find_content(contents_dir, request_path, content_extensions)
            if content_file is None:
                status_code = 404
                # try 404 content, fallback to built-in message
                error_file = _find_content(contents_dir, "/404", content_extensions)
                if error_file:
                    content_html = _render_file(error_file)
                    content_html = _process_snippets(content_html, snippets_dir)
                else:
                    content_html = "<h1>404 &mdash; Page not found</h1>"
            else:
                content_html = _render_file(content_file)
                content_html = _process_snippets(content_html, snippets_dir)
        # template (hierarchical lookup)
        template_file: Optional[Path] = None
        if templates_dir.is_dir():
            template_file = _find_template(
                templates_dir, request_path, default_template, template_extensions
            )
        html = _build_response(template_file, content_html, snippets_dir)
        return HTMLResponse(content=html, status_code=status_code)
    return app

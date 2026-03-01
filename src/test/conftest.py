from pathlib import Path
import pytest
from etomyte.core.app import Etomyte
from etomyte.core.cms import CMS
from etomyte.core.server import Server
from etomyte.adapter.file import FileAdapter


def _ensure_sample_project(home_path: Path) -> None:
    (home_path / "config").mkdir(parents=True, exist_ok=True)
    (home_path / "contents" / "product" / "cars").mkdir(parents=True, exist_ok=True)
    (home_path / "templates" / "product" / "cars").mkdir(parents=True, exist_ok=True)
    (home_path / "snippets").mkdir(parents=True, exist_ok=True)

    (home_path / "contents" / "test.md").write_text("Test page", encoding="utf-8")
    (home_path / "contents" / "product" / "cars" / "MyCar.md").write_text("Test", encoding="utf-8")

    (home_path / "templates" / "index.md").write_text(
        "Template index.md content\n\n{{content}}\n",
        encoding="utf-8",
    )
    (home_path / "templates" / "product" / "cars" / "MyCar.md").write_text(
        "About cars template",
        encoding="utf-8",
    )

    (home_path / "snippets" / "about_cars.py").write_text(
        'result = "About cars"',
        encoding="utf-8",
    )

    (home_path / "config" / "config.py").write_text(
        'HOST = "127.0.0.1"\nPORT = 8000\nDEFAULT_TEMPLATE = "index"\n',
        encoding="utf-8",
    )
    (home_path / "config" / "routes.py").write_text(
        'from etomyte.core.route import route\n\n@route("GET", "/hello")\nasync def hello():\n    return {"message": "hello"}\n\n@route("POST", "/data")\nasync def data():\n    return {"ok": True}\n',
        encoding="utf-8",
    )

@pytest.fixture
def home():
    """
    Caminho base do projeto de teste (ETOMYTE_HOME).
    """
    BASE_DIR = Path(__file__).resolve().parent
    project_home = BASE_DIR/"sample_project"
    _ensure_sample_project(project_home)
    ETOMYTE_HOME = str(project_home)
    return ETOMYTE_HOME

@pytest.fixture
def adapter(home):
    """
    Instância FileAdapter apontando para o projecto de teste.
    """
    return FileAdapter(home)

@pytest.fixture
def cms(home):
    """
    Instância CMS com FileAdapter apontando para o projecto de teste.
    """
    return CMS(adapter=FileAdapter(home))

@pytest.fixture
def cms_with_default_template(home):
    """Instância CMS com template padrão 'index'."""
    return CMS(adapter=FileAdapter(home=home), default_template="index")

@pytest.fixture
def server(home):
    """
    Instância Server com BASE_PATH configurado.
    """
    server = Server(port=8000)
    return server

@pytest.fixture
def app(home, adapter, server):
    """
    Instância Etomyte configurada para testes."""
    app = Etomyte(home=home
        , adapter=adapter
        , host=server.host
        , port=server.port)
    return app
import pytest
from etomyte.core.app import Etomyte
from etomyte.core.cms import CMS
from etomyte.core.server import Server
from etomyte.adapter.file import FileAdapter

ETOMYTE_HOME = "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX"

@pytest.fixture
def home():
    """
    Caminho base do projeto de teste (ETOMYTE_HOME).
    """
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
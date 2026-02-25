import pytest
from etomyte.core.cms import CMS
from git_repo.src.etomyte.core.server import Server
from etomyte.adapter.file import FileAdapter

def test_get_template():
    server = Server(port=8000)
    server.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    app = CMS(server, adapter=FileAdapter(server))
    assert app.get_template("/product/cars/MyCar") == "About cars template"
    assert app.get_template("/") == "Index template"
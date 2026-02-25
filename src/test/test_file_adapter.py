import pytest
from etomyte.core.cms import CMS
from git_repo.src.etomyte.core.server import Server
from etomyte.adapter.file import FileAdapter

def test_get_template():
    app = Server(port=8000)
    app.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    cms = CMS(app, adapter=FileAdapter(app))
    assert cms.get_template("/product/cars/MyCar") == "About cars template"
    result = cms.get_template("/product/cars")
    assert result == "Index template"
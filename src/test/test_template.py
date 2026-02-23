import pytest
from etomyte.core.cms import CMS
from etomyte.core.server import App
from etomyte.adapter.file import FileAdapter

def test_get_template():
    app = App(port=8000)
    app.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    cms = CMS(app, adapter=FileAdapter(app))
    assert cms.get_template("/product/cars/MyCar") == "About cars template"
    assert cms.get_template("/") == "Index template"
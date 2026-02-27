from etomyte.core.cms import CMS
from etomyte.adapter.file import FileAdapter

def test_get_content():
    home = "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX"
    app = CMS(adapter=FileAdapter(home))
    assert app.get_content("/test") == "Test page"
    assert app.get_content("/product/cars/MyCar") == "Test"
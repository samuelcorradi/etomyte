import pytest
from etomyte.core.cms import CMS
from git_repo.src.etomyte.core.server import Server
from etomyte.adapter.file import FileAdapter

def test_exec_snippet():
    app = Server(port=8000)
    app.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    cms = CMS(app, adapter=FileAdapter(app))
    assert cms.exec_snippet("result=a", {'a': 'About cars template'}) == "About cars template"
    assert cms.exec_snippet("result = a.upper()", {'a': 'About cars template'}) == "ABOUT CARS TEMPLATE"

def test_get_snippet():
    app = Server(port=8000)
    app.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    cms = CMS(app, adapter=FileAdapter(app))
    assert cms.get_snippet("about_cars") == "result = \"About cars\""
    
def test_process_snippets():
    app = Server(port=8000)
    app.set_config("BASE_PATH", "C:\\Users\\samue\\OneDrive - Nortegra\\workspace\\etomyte\\projectX")
    cms = CMS(app, adapter=FileAdapter(app))
    doc_text = """
Welcome to our site! [[about_cars]] Enjoy your stay.

"""
    expected = """
Welcome to our site! About cars Enjoy your stay.

"""
    assert cms.process_snippets(doc_text) == expected
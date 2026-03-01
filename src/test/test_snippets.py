def test_exec_snippet(cms):
    assert cms.exec_snippet("result=a", {'a': 'About cars template'}) == "About cars template"
    assert cms.exec_snippet("result = a.upper()", {'a': 'About cars template'}) == "ABOUT CARS TEMPLATE"

def test_get_snippet(cms):
    assert cms.get_snippet("about_cars") == "result = \"About cars\""
    
def test_process_snippets(cms):
    doc_text = """
Welcome to our site! [[about_cars]] Enjoy your stay.

"""
    expected = """
Welcome to our site! About cars Enjoy your stay.

"""
    assert cms.process_snippets(doc_text) == expected
import pytest

def test_get_template(cms):
    assert cms.get_template("/product/cars/MyCar") == "About cars template"

def test_get_template_fallback(cms):
    result = cms.get_template("/product/cars")
    assert result == """Template index.md content

{{content}}
"""
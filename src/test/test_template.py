def test_get_template(cms_with_default_template):
    cms = cms_with_default_template
    #
    assert cms.get_template("/product/cars/MyCar") == "About cars template"
    #
    assert cms.get_template("/") == """Template index.md content

{{content}}
"""
    #
    cms.default_template = "nonexistent"
    assert cms.get_template("/nonexistent") == "{{content}}"
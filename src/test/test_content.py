def test_get_content(cms):
    assert cms.get_content("/test") == "Test page"
    assert cms.get_content("/product/cars/MyCar") == "Test"
import pytest

@pytest.mark.regression
def test_checkout_regression(env, browser):
    print(f"Regression test | env={env}, browser={browser}")
    assert True

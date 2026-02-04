import pytest

@pytest.mark.smoke
def test_login_smoke(env, browser):
    print(f"Smoke test | env={env}, browser={browser}")
    assert True

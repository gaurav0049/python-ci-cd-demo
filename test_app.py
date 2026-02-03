import pytest
from app import add

@pytest.mark.smoke
def test_add_smoke():
    assert add(2, 3) == 5

@pytest.mark.regression
def test_add_regression():
    assert add(5, 5) == 10
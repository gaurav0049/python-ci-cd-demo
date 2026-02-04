import pytest

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="qa")
    parser.addoption("--browser", action="store", default="chrome")

@pytest.fixture(scope="session")
def env(request):
    return request.config.getoption("--env")

@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")

import pytest

from sp import settings
from sp.common.utils import AppFileManager
from tests.fixtures.app import AppTester

FAKE_API_KEY = "FAKE-TEST-API-KEY"
HAS_REAL_API_KEY = bool(settings.API_KEY)
if not HAS_REAL_API_KEY:
    settings.API_KEY = FAKE_API_KEY


def pytest_configure(config):
    config.addinivalue_line("markers", "live: calls the real Silent Push API, needs SILENT_PUSH_API_KEY")


@pytest.fixture
def app(request):
    app = AppTester(application_manager=AppFileManager("test app"))
    app.skip_on_job = request.node.get_closest_marker("live") is not None
    app.fixture_setup()
    yield app
    app.fixture_teardown()


def pytest_collection_modifyitems(config, items):
    if HAS_REAL_API_KEY:
        return
    skip_live = pytest.mark.skip(reason="SILENT_PUSH_API_KEY not set")
    for item in items:
        if "live" in item.keywords:
            item.add_marker(skip_live)

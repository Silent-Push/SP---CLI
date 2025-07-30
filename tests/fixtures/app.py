import cmd2_ext_test
import pytest

from sp.common.utils import AppFileManager
from sp.main import App


class AppTester(cmd2_ext_test.ExternalTestMixin, App):
    pass


@pytest.fixture
def app():
    app = AppTester(application_manager=AppFileManager("test app"))
    app.fixture_setup()
    yield app
    app.fixture_teardown()

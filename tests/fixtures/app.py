import re

import cmd2_ext_test
import pytest

from sp.common.utils import AppFileManager
from sp.main import App

JOB_HINT = re.compile(r"`job (\S+)`")
"""The hint shown by BaseCommand.check_job when the API returns a job instead of results"""


class AppTester(cmd2_ext_test.ExternalTestMixin, App):
    skip_on_job = False
    """Live tests can't validate a job, so they're skipped instead of failing"""

    def app_cmd(self, command: str, echo=None):
        out = super().app_cmd(command, echo)
        job = JOB_HINT.search(out.stderr)
        if self.skip_on_job and job:
            pytest.skip(f"The API returned job {job.group(1)} instead of results, try later: `job {job.group(1)}`")
        return out


@pytest.fixture
def app(request):
    app = AppTester(application_manager=AppFileManager("test app"))
    app.skip_on_job = request.node.get_closest_marker("live") is not None
    app.fixture_setup()
    yield app
    app.fixture_teardown()

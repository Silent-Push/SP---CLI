import json
from unittest.mock import MagicMock, patch

import pytest

from tests.fixtures.app import app

JOB_ID = "01234567-0123-0123-abcd-0123456789ab"
JOB_STATUS = {"job_id": JOB_ID, "status": "STARTED"}
JOB_WARNING = f"`job {JOB_ID}`"


def mocked_response(body: dict) -> MagicMock:
    return MagicMock(status_code=200, content=json.dumps(body).encode())


@pytest.mark.parametrize(
    "command, target, body",
    [
        # newer endpoints return the job at the top level
        ("enrich ig.com", "sp.commands.base.enrich.requests.get", {"job_status": JOB_STATUS}),
        # older endpoints wrap it in "response"
        ("score ig.com", "sp.commands.score.requests.get", {"response": {"job_status": JOB_STATUS}}),
    ],
)
def test_job_response_shows_job_command(app, command, target, body):
    with patch(target, return_value=mocked_response(body)):
        out = app.app_cmd(command)
    assert JOB_WARNING in out.stderr
    assert json.loads(out.stdout) == JOB_STATUS


def test_job_command_calls_job_endpoint(app):
    with patch("sp.commands.base.job.requests.get", return_value=mocked_response({"records": []})) as get:
        out = app.app_cmd(f"job {JOB_ID}")
    assert get.call_args.args[0].endswith(f"v1/explore/job/{JOB_ID}/")
    assert json.loads(out.stdout) == {"records": []}


def test_job_command_requires_job_id(app):
    out = app.app_cmd("job")
    assert "job_id" in out.stderr


@pytest.mark.live
def test_live_test_is_skipped_when_api_returns_job(app):
    with patch("sp.commands.score.requests.get",
               return_value=mocked_response({"response": {"job_status": JOB_STATUS}})):
        app.app_cmd("score ig.com -v")
    pytest.fail("a live test should be skipped when the API returns a job")

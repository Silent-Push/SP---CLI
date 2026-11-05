import json
from unittest.mock import MagicMock, patch

import pytest

from tests.fixtures.app import API_REQUEST, app

JOB_ID = "01234567-0123-0123-abcd-0123456789ab"
JOB_STATUS = {"job_id": JOB_ID, "status": "STARTED"}
JOB_WARNING = f"`job {JOB_ID}`"


def mocked_response(body: dict) -> MagicMock:
    return MagicMock(status_code=200, content=json.dumps(body).encode())


@pytest.mark.parametrize(
    "command, body",
    [
        # newer endpoints return the job at the top level
        ("enrich ig.com", {"job_status": JOB_STATUS}),
        # older endpoints wrap it in "response"
        ("score ig.com", {"response": {"job_status": JOB_STATUS}}),
    ],
)
def test_job_response_shows_job_command(app, command, body):
    with patch(API_REQUEST, return_value=mocked_response(body)):
        out = app.app_cmd(command)
    assert JOB_WARNING in out.stderr
    assert out.stdout == ""


def test_job_command_calls_job_endpoint(app):
    with patch(API_REQUEST, return_value=mocked_response({"records": []})) as request:
        out = app.app_cmd(f"job {JOB_ID}")
    assert request.call_args.args[1].endswith(f"v1/explore/job/{JOB_ID}/")
    assert json.loads(out.stdout) == {"records": []}


def test_job_command_requires_job_id(app):
    out = app.app_cmd("job")
    assert "job_id" in out.stderr


@pytest.mark.live
def test_live_test_is_skipped_when_api_returns_job(app):
    with patch(API_REQUEST, return_value=mocked_response({"response": {"job_status": JOB_STATUS}})):
        app.app_cmd("score ig.com -v")
    pytest.fail("a live test should be skipped when the API returns a job")

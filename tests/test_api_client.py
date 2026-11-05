import json
from unittest.mock import MagicMock, patch

import pytest
import requests

from sp import settings
from sp.common.api import RETRY_STATUSES, USER_AGENT, api
from sp.main import main
from tests.fixtures.app import API_REQUEST


def mocked_response(status_code: int, body, headers: dict = None) -> MagicMock:
    content = body if isinstance(body, bytes) else json.dumps(body).encode()
    return MagicMock(status_code=status_code, content=content, headers=headers or {})


def test_request_sends_key_timeout_and_user_agent():
    with patch.object(api.session, "request") as request:
        api.request("POST", "https://api.example/v1/x", {"a": 1})
    kwargs = request.call_args.kwargs
    assert kwargs["headers"] == {"x-api-key": settings.API_KEY}
    assert kwargs["timeout"] == settings.API_TIMEOUT
    assert kwargs["json"] == {"a": 1}
    assert api.session.headers["User-Agent"] == USER_AGENT


def test_retries_rate_limits_and_server_errors():
    retry = api.session.get_adapter("https://api.silentpush.com").max_retries
    assert retry.total == 3
    assert set(retry.status_forcelist) == set(RETRY_STATUSES)
    assert retry.allowed_methods is None  # POST queries are retried too


def test_timeout_stops_command(app):
    with patch(API_REQUEST, side_effect=requests.Timeout):
        out = app.app_cmd("score ig.com")
    assert out.stdout == ""
    assert "didn't answer" in out.stderr


def test_connection_error_stops_command(app):
    with patch(API_REQUEST, side_effect=requests.ConnectionError):
        out = app.app_cmd("score ig.com")
    assert out.stdout == ""
    assert "Can't reach the Silent Push API" in out.stderr


@pytest.mark.parametrize(
    "status_code, headers, hint",
    [
        (401, {}, "Is your API key correct?"),
        (403, {}, "Is your API key correct?"),
        (404, {}, "Not found"),
        (429, {"Retry-After": "30"}, "Rate limited, try again in 30s"),
        (429, {}, "Rate limited, try again later"),
        (503, {}, "having problems"),
        (400, {}, "Check the command options"),
    ],
)
def test_error_hint_matches_status(app, status_code, headers, hint):
    response = mocked_response(status_code, {"errors": [{"code": "x"}]}, headers)
    with patch(API_REQUEST, return_value=response):
        out = app.app_cmd("score ig.com")
    assert hint in out.stderr
    if status_code not in (401, 403):
        assert "API key" not in out.stderr  # used to blame the key for every error


def test_unexpected_exceptions_are_still_reported(app):
    with patch(API_REQUEST, side_effect=ZeroDivisionError("a real bug")):
        out = app.app_cmd("score ig.com")
    assert "EXCEPTION of type 'ZeroDivisionError'" in out.stderr


@pytest.mark.parametrize("command", ["score ig.com", "enrich ig.com", "threatcheck ig.com", "whoislive ig.com"])
def test_invalid_json_stops_command(app, command):
    with patch(API_REQUEST, return_value=mocked_response(200, b"not json")):
        out = app.app_cmd(command)
    assert out.stdout == ""
    assert "Can't parse command response" in out.stderr


def test_enrich_ip_without_ip2asn(app):
    with patch(API_REQUEST, return_value=mocked_response(200, {"response": {}})):
        out = app.app_cmd("enrich 8.8.8.8")
    assert out.stdout == ""
    assert "Can't parse command response" in out.stderr


def test_error_message_from_json_and_html(app):
    with patch(API_REQUEST, return_value=mocked_response(401, {"errors": [{"code": "not_authenticated"}]})):
        out = app.app_cmd("score ig.com")
    assert "Status Code 401: [{'code': 'not_authenticated'}]" in out.stderr  # no stray "}" anymore
    html = b"<html><head><title>x</title></head><body><h1>Bad Gateway</h1></body></html>"
    with patch(API_REQUEST, return_value=mocked_response(502, html)):
        out = app.app_cmd("score ig.com")
    assert "Status Code 502: Bad Gateway" in out.stderr


@pytest.mark.parametrize(
    "argv, response, exit_code",
    [
        (["help"], None, 0),
        (["score", "notanioc"], None, 1),
        (["score", "ig.com"], mocked_response(200, {"response": {"sp_risk_score": 5}}), 0),
        (["score", "ig.com"], mocked_response(401, {"errors": []}), 1),
        (["foo"], None, 1),
        # a job isn't a failure, the warning used to make `sp` exit with 1
        (["score", "ig.com"], mocked_response(200, {"response": {"job_status": {"job_id": "1"}}}), 0),
    ],
)
def test_exit_code(argv, response, exit_code):
    with patch(API_REQUEST, return_value=response):
        assert main(argv) == exit_code

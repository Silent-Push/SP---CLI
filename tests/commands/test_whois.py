import json
from unittest.mock import MagicMock, patch

import jsonschema
import pytest
from cmd2 import CommandResult

from tests.fixtures.app import API_REQUEST, app

whois_result_schema = {
    "type": "object",
    "required": ["domain", "registrar", "created", "expires", "updated", "nameservers", "whois_server", "raw"],
    "properties": {
        "domain": {"type": "string"},
        "registrar": {"type": "string"},
        "created": {"type": "string"},
        "expires": {"type": "string"},
        "updated": {"type": "string"},
        "nameservers": {"type": "array"},
        "whois_server": {"type": "string"},
        "raw": {"type": "object"},
    },
}


def mocked_response(whois: dict) -> MagicMock:
    content = json.dumps({"status_code": 200, "error": None, "response": {"whois_live": whois}}).encode()
    return MagicMock(status_code=200, content=content)


@pytest.mark.live
def test_whoislive(app):
    out = app.app_cmd("whoislive silentpush.com")
    assert isinstance(out, CommandResult)
    whois_result = json.loads(out.stdout)
    jsonschema.validate(instance=whois_result, schema=whois_result_schema)
    assert whois_result["domain"] == "silentpush.com"


def test_whoislive_calls_domain_endpoint(app):
    with patch(API_REQUEST, return_value=mocked_response({"domain": "ig.com"})) as request:
        out = app.app_cmd("whoislive ig.com")
    assert request.call_args.args[1].endswith("v1/explore/domain/whoislive/ig.com/")
    assert json.loads(out.stdout) == {"domain": "ig.com"}


def test_whoislive_without_results(app):
    with patch(API_REQUEST, return_value=mocked_response({})):
        out = app.app_cmd("whoislive unknown-domain.com")
    assert out.stdout == ""
    assert "No whois information found for unknown-domain.com" in out.stderr


@pytest.mark.parametrize("ioc", ["8.8.8.8", "https://ig.com/a"])
def test_whoislive_only_accepts_domains(app, ioc):
    with patch(API_REQUEST) as request:
        out = app.app_cmd(f"whoislive {ioc}")
    request.assert_not_called()
    assert f"'{ioc}' is not a domain" in out.stderr


def test_whoislive_adds_domain_to_autocomplete(app):
    app._ioc_cache = []
    with patch(API_REQUEST, return_value=mocked_response({"domain": "ig.com"})):
        app.app_cmd("whoislive ig.com")
    assert app._ioc_cache == ["ig.com"]

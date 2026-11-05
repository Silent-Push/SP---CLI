import json
import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

import pytest

from sp.main import main
from tests.fixtures.app import API_REQUEST


def test_add_list_of_iocs_to_cache(app):
    app._ioc_cache = ["a.com"]
    app._add_ioc_to_cache(["a.com", "b.com"])
    app._add_ioc_to_cache("c.com")
    assert app._ioc_cache == ["a.com", "b.com", "c.com"]


def test_unload_before_load(app):
    out = app.app_cmd("unload padns")
    assert "EXCEPTION" not in out.stderr
    assert "PADNS is not loaded" in out.stderr


def test_load_then_unload(app):
    app.app_cmd("load padns")
    out = app.app_cmd("unload padns")
    assert "PADNS unloaded" in out.stdout
    assert "EXCEPTION" not in out.stderr
    assert app.LOADED_COMMAND == ""


def test_spql_command_without_query():
    main(["websearch"])  # used to raise IndexError


@pytest.mark.parametrize("command", ["websearch", "feedsearch"])
def test_spql_command_without_query_shows_message(app, command):
    app.interactive = False
    with patch(API_REQUEST) as request:
        out = app.app_cmd(f"{command}\n")
    request.assert_not_called()
    assert out.stdout == ""
    assert out.stderr == "You need to specify a query\n"  # used to raise ValueError


def test_single_command_does_not_wait_for_multiline_input():
    with patch("sp.main.App.onecmd_plus_hooks", autospec=True) as onecmd:
        main(["websearch", 'domain="ig.com"'])
    assert onecmd.call_args.args[1].endswith("\n")  # without it, cmd2 shows a "> " prompt


def test_help_works_without_api_key():
    env = {k: v for k, v in os.environ.items() if k != "SILENT_PUSH_API_KEY"}
    result = subprocess.run(
        [sys.executable, "-c", "from sp.main import main; main(['help'])"],
        env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_command_without_api_key_shows_message(app, monkeypatch):
    monkeypatch.setattr("sp.settings.API_KEY", None)
    with patch(API_REQUEST) as request:
        out = app.app_cmd("score ig.com")
    request.assert_not_called()
    assert "SILENT_PUSH_API_KEY" in out.stderr
    assert "EXCEPTION" not in out.stderr


def test_score_ip_with_empty_result(app):
    content = json.dumps({"response": {"ip2asn": []}}).encode()
    response = MagicMock(status_code=200, content=content)
    with patch(API_REQUEST, return_value=response):
        out = app.app_cmd("score 1.2.3.4")
    assert "Can't parse command response" in out.stderr
    assert "AttributeError" not in out.stderr


def test_threatcheck_with_empty_result(app):
    response = MagicMock(status_code=200, content=b'{"listed_details": []}')
    with patch(API_REQUEST, return_value=response):
        out = app.app_cmd("threatcheck ig.com")
    assert "Can't parse command response" in out.stderr
    assert "AttributeError" not in out.stderr


def test_websearch_default_sort(app):
    app.interactive = False
    content = json.dumps({"response": {"scandata_raw": []}}).encode()
    response = MagicMock(status_code=200, content=content)
    with patch(API_REQUEST, return_value=response) as request:
        app.app_cmd("websearch 'domain=\"ig.com\"'\n")
    assert request.call_args.args[2]["sorting"] == ["scan_date/desc"]


def test_load_unload_load_again(app):
    app.app_cmd("load padns")
    app.app_cmd("unload padns")
    out = app.app_cmd("load padns")
    assert "PADNS loaded" in out.stdout
    assert "EXCEPTION" not in out.stderr
    assert app.LOADED_COMMAND == "padns"


def test_api_error_stops_command(app):
    content = json.dumps({"errors": [{"code": "not_authenticated"}]}).encode()
    response = MagicMock(status_code=401, content=content)
    with patch(API_REQUEST, return_value=response):
        out = app.app_cmd("score ig.com")
    assert out.stdout == ""  # used to print the error body as if it was the result
    assert "Something went wrong :(" in out.stderr
    assert "Can't parse command response" not in out.stderr

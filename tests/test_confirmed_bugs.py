import json
import os
import subprocess
import sys
from unittest.mock import MagicMock, patch

from sp.main import main
from tests.fixtures.app import app


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


def test_help_works_without_api_key():
    env = {k: v for k, v in os.environ.items() if k != "SILENT_PUSH_API_KEY"}
    result = subprocess.run(
        [sys.executable, "-c", "from sp.main import main; main(['help'])"],
        env=env, capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr


def test_command_without_api_key_shows_message(app, monkeypatch):
    monkeypatch.setattr("sp.settings.API_KEY", None)
    with patch("sp.commands.score.requests.get") as get:
        out = app.app_cmd("score ig.com")
    get.assert_not_called()
    assert "SILENT_PUSH_API_KEY" in out.stderr


def test_score_ip_with_empty_result(app):
    content = json.dumps({"response": {"ip2asn": []}}).encode()
    response = MagicMock(status_code=200, content=content)
    with patch("sp.commands.score.requests.get", return_value=response):
        out = app.app_cmd("score 1.2.3.4")
    assert "Can't parse command response" in out.stderr
    assert "AttributeError" not in out.stderr


def test_threatcheck_with_empty_result(app):
    response = MagicMock(status_code=200, content=b'{"listed_details": []}')
    with patch("sp.commands.base.threatcheck.requests.get", return_value=response):
        out = app.app_cmd("threatcheck ig.com")
    assert "Can't parse command response" in out.stderr
    assert "AttributeError" not in out.stderr


def test_websearch_default_sort(app):
    app.interactive = False
    content = json.dumps({"response": {"scandata_raw": []}}).encode()
    response = MagicMock(status_code=200, content=content)
    with patch("sp.commands.base.spql.requests.post", return_value=response) as post:
        app.app_cmd("websearch 'domain=\"ig.com\"'\n")
    assert post.call_args.kwargs["json"]["sorting"] == ["scan_date/desc"]


def test_load_unload_load_again(app):
    app.app_cmd("load padns")
    app.app_cmd("unload padns")
    out = app.app_cmd("load padns")
    assert "PADNS loaded" in out.stdout
    assert "EXCEPTION" not in out.stderr
    assert app.LOADED_COMMAND == "padns"

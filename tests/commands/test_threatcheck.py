import json

import jsonschema
import pytest
from cmd2 import CommandResult

from tests.fixtures.app import app

pytestmark = pytest.mark.live

threatcheck_verbose_result_schema = {
    "type": "object",
    "required": ["value", "parsed", "type", "data_source", "is_listed", "cnames", "listed_details", "error"],
    "properties": {
        "value": {"type": "string"},
        "parsed": {"type": "string"},
        "type": {"type": "string"},
        "data_source": {"type": "string"},
        "is_listed": {"type": "boolean"},
        "cnames": {"type": "array"},
        "listed_details": {"type": "array"},
        "error": {"type": "string"},
    },
}


def test_threatcheck_domain(app):
    out = app.app_cmd("threatcheck silentpush.com")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, str)
    assert threatcheck_result == "no listing"


def test_bulk_threatcheck_domain(app):
    out = app.app_cmd("bulk_threatcheck silentpush.com microsoft.com")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, list)
    threatcheck_result_schema = {
        "type": "array",
        "items": {"type": "object"}
    }
    jsonschema.validate(instance=threatcheck_result, schema=threatcheck_result_schema)


def test_threatcheck_domain_verbose(app):
    out = app.app_cmd("threatcheck silentpush.com -v")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, dict)
    jsonschema.validate(instance=threatcheck_result, schema=threatcheck_verbose_result_schema)


def test_bulk_threatcheck_domain_verbose(app):
    out = app.app_cmd("bulk_threatcheck silentpush.com microsoft.com -v")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, list)
    jsonschema.validate(
        instance=threatcheck_result,
        schema={"type": "array", "items": threatcheck_verbose_result_schema},
    )


def test_threatcheck_ip(app):
    out = app.app_cmd("threatcheck 8.8.4.4")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, str)
    assert threatcheck_result == "no listing"


def test_bulk_threatcheck_ip(app):
    out = app.app_cmd("bulk_threatcheck 8.8.4.4 8.8.8.8")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, list)
    threatcheck_result_schema = {
        "type": "array",
        "items": {"type": "object"}
    }
    jsonschema.validate(instance=threatcheck_result, schema=threatcheck_result_schema)


def test_threatcheck_ip_verbose(app):
    out = app.app_cmd("threatcheck 8.8.4.4 -v")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, dict)
    jsonschema.validate(instance=threatcheck_result, schema=threatcheck_verbose_result_schema)


def test_bulk_threatcheck_ip_verbose(app):
    out = app.app_cmd("bulk_threatcheck 8.8.4.4 8.8.8.8 -v")
    assert isinstance(out, CommandResult)
    threatcheck_result = json.loads(out.stdout)
    assert isinstance(threatcheck_result, list)
    jsonschema.validate(
        instance=threatcheck_result,
        schema={"type": "array", "items": threatcheck_verbose_result_schema},
    )

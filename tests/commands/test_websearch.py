import json

import jsonschema
import pytest
from cmd2 import CommandResult

from tests.fixtures.app import app

pytestmark = pytest.mark.live


def test_websearch(app):
    app.interactive = False
    websearch_result_schema = {
        "type": "array",
        "items": {"type": "object"},  # too many properties to validate
    }
    out = app.app_cmd("websearch 'domain=\"microsoft.com\"'\n")
    assert isinstance(out, CommandResult)
    websearch_result = json.loads(out.stdout)
    assert isinstance(websearch_result, list)
    jsonschema.validate(instance=websearch_result, schema=websearch_result_schema)
    properties = websearch_result[0].keys()
    assert "datasource" in properties
    assert "scan_date" in properties
    assert "user-agent" in properties
    assert "response" in properties
    assert "port" in properties
    assert "ip" in properties
    assert "hostname" in properties

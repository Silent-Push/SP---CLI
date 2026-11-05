import json

import jsonschema
import pytest
from cmd2 import CommandResult

pytestmark = pytest.mark.live


def test_feedsearch(app):
    app.interactive = False
    feedsearch_result_schema = {
        "type": "array",
        "items": {"type": "object"},  # too many properties to validate
    }
    out = app.app_cmd("feedsearch 'vendor=\"Silent Push\"'\n")
    assert isinstance(out, CommandResult)
    feedsearch_result = json.loads(out.stdout)
    assert isinstance(feedsearch_result, list)
    jsonschema.validate(instance=feedsearch_result, schema=feedsearch_result_schema)
    properties = feedsearch_result[0].keys()
    assert "datasource" in properties
    assert "sp_risk_score" in properties
    assert "type" in properties
    assert "vendor" in properties
    assert "indicator" in properties
    assert "feed" in properties

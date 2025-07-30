import json

import jsonschema
from cmd2 import CommandResult

from tests.fixtures.app import app


def test_score(app):
    out = app.app_cmd("score silentpush.com")
    assert isinstance(out, CommandResult)
    score_result = json.loads(out.stdout)
    assert isinstance(score_result, dict)
    score_result_schema = {
        "type": "object",
        "properties": {
            "domain": {"type": "string"},
            "sp_risk_score": {"type": "number"},
            "sp_risk_score_explain": {"type": "object"},
        },
    }
    jsonschema.validate(instance=score_result, schema=score_result_schema)

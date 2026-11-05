import json

import jsonschema
import pytest
from cmd2 import CommandResult

pytestmark = pytest.mark.live

score_explain_properties = {
    "sp_risk_score": {"type": "number"},
    "sp_risk_score_explain": {
        "type": "object",
        "required": ["sp_risk_score_decider"],
        "properties": {"sp_risk_score_decider": {"type": "string"}},
    },
}
"""Score properties shared by domain and ip verbose results"""

score_domain_verbose_result_schema = {
    "type": "object",
    "required": ["domain", "sp_risk_score", "sp_risk_score_explain"],
    "properties": {"domain": {"type": "string"}, **score_explain_properties},
}

score_ip_verbose_result_schema = {
    "type": "object",
    "required": ["ip2asn"],
    "properties": {
        "ip2asn": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "required": ["ip", "sp_risk_score", "sp_risk_score_explain"],
                "properties": {"ip": {"type": "string"}, **score_explain_properties},
            },
        },
    },
}


def test_score_domain(app):
    out = app.app_cmd("score silentpush.com")
    assert isinstance(out, CommandResult)
    score_result = json.loads(out.stdout)
    assert isinstance(score_result, int)


def test_score_domain_verbose(app):
    out = app.app_cmd("score silentpush.com -v")
    assert isinstance(out, CommandResult)
    score_result = json.loads(out.stdout)
    assert isinstance(score_result, dict)
    jsonschema.validate(instance=score_result, schema=score_domain_verbose_result_schema)
    assert score_result["domain"] == "silentpush.com"


def test_score_ip(app):
    out = app.app_cmd("score 8.8.4.4")
    assert isinstance(out, CommandResult)
    score_result = json.loads(out.stdout)
    assert isinstance(score_result, int)


def test_score_ip_verbose(app):
    out = app.app_cmd("score 8.8.4.4 -v")
    assert isinstance(out, CommandResult)
    score_result = json.loads(out.stdout)
    assert isinstance(score_result, dict)
    jsonschema.validate(instance=score_result, schema=score_ip_verbose_result_schema)
    assert score_result["ip2asn"][0]["ip"] == "8.8.4.4"

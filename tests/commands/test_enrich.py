import json
import jsonschema

from cmd2 import CommandResult
from tests.fixtures.app import app

enrich_result_schema = {
    "type": "object",
    "properties": {
        "domain_string_frequency_probability": {"type": "object"},
        "domain_urls": {"type": "object"},
        "domaininfo": {"type": "object"},
        "host_flags": {"type": "array"},
        "ip_diversity": {"type": "object"},
        "is_private_suffix": {"type": "boolean"},
        "listing_score": {"type": "number"},
        "ns_reputation": {"type": "object"},
        "nschanges": {"type": "object"},
        "private_suffix_info": {"type": "object"},
        "sp_risk_score": {"type": "number"}
    },
}


def test_enrich(app):
    out = app.app_cmd("enrich silentpush.com")
    assert isinstance(out, CommandResult)
    enrich_result = json.loads(out.stdout)
    assert isinstance(enrich_result, dict)
    jsonschema.validate(instance=enrich_result, schema=enrich_result_schema)


def test_bulk_enrich(app):
    out = app.app_cmd("bulk_enrich silentpush.com google.com")
    assert isinstance(out, CommandResult)
    bulk_enrich_result = json.loads(out.stdout)
    assert isinstance(bulk_enrich_result, list)
    bulk_enrich_result_schema = {
        "type": "array",
        "items": {
            **enrich_result_schema
        }
    }
    jsonschema.validate(instance=bulk_enrich_result, schema=bulk_enrich_result_schema)

import json
from unittest.mock import patch

import jsonschema
import pytest
from cmd2 import CommandResult

from tests.fixtures.app import app

enrich_domain_result_schema = {
    "type": "object",
    "required": [
        "domain_string_frequency_probability", "domain_urls", "domaininfo",
        "host_flags", "ip_diversity", "is_private_suffix", "listing_score",
        "ns_reputation", "nschanges", "private_suffix_info", "sp_risk_score",
    ],
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
        "sp_risk_score": {"type": "number"},
    },
}

enrich_ip_result_schema = {
    "type": "object",
    "required": ["ip", "asn", "asname", "subnet", "ip_location", "ip_flags", "listing_score", "sp_risk_score"],
    "properties": {
        "ip": {"type": "string"},
        "asn": {"type": "number"},
        "asname": {"type": "string"},
        "subnet": {"type": "string"},
        "ip_location": {"type": "object"},
        "ip_flags": {"type": "object"},
        "listing_score": {"type": "number"},
        "sp_risk_score": {"type": "number"},
    },
}

enrich_domain_output_keys = {"sp_risk_score", "listing_score", "is_private_suffix"}
"""Top level keys expected as rows in the csv/tsv output"""


def get_output_keys(output: str, separator=None) -> set:
    """The first column of each csv/tsv output row"""
    return {line.split(separator, 1)[0] for line in output.splitlines() if line.strip()}


@pytest.mark.live
def test_enrich_domain(app):
    out = app.app_cmd("enrich silentpush.com")
    assert isinstance(out, CommandResult)
    enrich_result = json.loads(out.stdout)
    assert isinstance(enrich_result, dict)
    jsonschema.validate(instance=enrich_result, schema=enrich_domain_result_schema)


@pytest.mark.live
def test_enrich_domain_json_output(app):
    out = app.app_cmd("enrich silentpush.com -j")
    assert isinstance(out, CommandResult)
    assert isinstance(out.stdout, str)
    jsonschema.validate(instance=json.loads(out.stdout), schema=enrich_domain_result_schema)


@pytest.mark.live
def test_enrich_domain_csv_output(app):
    out = app.app_cmd("enrich silentpush.com -c")
    assert isinstance(out, CommandResult)
    assert isinstance(out.stdout, str)
    assert enrich_domain_output_keys <= get_output_keys(out.stdout, ",")


@pytest.mark.live
def test_enrich_domain_tsv_output(app):
    out = app.app_cmd("enrich silentpush.com -t")
    assert isinstance(out, CommandResult)
    assert isinstance(out.stdout, str)
    assert enrich_domain_output_keys <= get_output_keys(out.stdout)


@pytest.mark.live
def test_bulk_enrich_domain(app):
    out = app.app_cmd("bulk_enrich silentpush.com google.com")
    assert isinstance(out, CommandResult)
    bulk_enrich_result = json.loads(out.stdout)
    assert isinstance(bulk_enrich_result, list)
    bulk_enrich_result_schema = {"type": "array", "items": {**enrich_domain_result_schema}}
    jsonschema.validate(instance=bulk_enrich_result, schema=bulk_enrich_result_schema)


@pytest.mark.live
def test_enrich_ip(app):
    out = app.app_cmd("enrich 8.8.4.4")
    assert isinstance(out, CommandResult)
    enrich_result = json.loads(out.stdout)
    assert isinstance(enrich_result, dict)
    jsonschema.validate(instance=enrich_result, schema=enrich_ip_result_schema)


@pytest.mark.live
def test_bulk_enrich_ip(app):
    out = app.app_cmd("bulk_enrich 8.8.4.4 8.8.8.8")
    assert isinstance(out, CommandResult)
    bulk_enrich_result = json.loads(out.stdout)
    assert isinstance(bulk_enrich_result, list)
    bulk_enrich_result_schema = {"type": "array", "items": {**enrich_ip_result_schema}}
    jsonschema.validate(instance=bulk_enrich_result, schema=bulk_enrich_result_schema)


def test_invalid_ioc(app):
    out = app.app_cmd("enrich 0")
    assert isinstance(out, CommandResult)
    enrich_result = out.stdout
    error_result = out.stderr
    assert isinstance(enrich_result, str)
    assert enrich_result == ''
    assert error_result == 'Not a valid IoC\n'


@patch("sp.commands.base.enrich.requests.get")
def test_error_handling(mocked_get, app):
    mocked_get.return_value.status_code = 400
    mocked_get.return_value.content = b"error"
    out = app.app_cmd("enrich ig.com")
    assert isinstance(out, CommandResult)
    error_result = out.stderr
    assert error_result.startswith("Something went wrong")

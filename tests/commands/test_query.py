import json
import jsonschema

from cmd2 import CommandResult
from tests.fixtures.app import app

common_properties = {
    "answer": {"type": "string"},
    "count": {"type": "number"},
    "first_seen": {"type": "string", "format": "date-time"},
    "last_seen": {"type": "string", "format": "date-time"},
    "query": {"type": "string"},
    "type": {"type": "string"},
}


def get_query_result_schema(properties: dict = common_properties):
    return {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        **properties
                    }
                }
            }
        }
    }


def test_query_a(app):
    out = app.app_cmd("query a silentpush.com")
    assert isinstance(out, CommandResult)
    query_a_result = json.loads(out.stdout)
    assert isinstance(query_a_result, dict)
    jsonschema.validate(instance=query_a_result, schema=get_query_result_schema())


def test_query_aaaa(app):
    out = app.app_cmd("query aaaa silentpush.com")
    assert isinstance(out, CommandResult)
    query_aaaa_result = json.loads(out.stdout)
    assert isinstance(query_aaaa_result, dict)
    jsonschema.validate(instance=query_aaaa_result, schema=get_query_result_schema())


def test_query_any(app):
    out = app.app_cmd("query any silentpush.com")
    assert isinstance(out, CommandResult)
    query_any_result = json.loads(out.stdout)
    assert isinstance(query_any_result, dict)
    jsonschema.validate(instance=query_any_result, schema=get_query_result_schema())


def test_query_anyipv4(app):
    out = app.app_cmd("query anyipv4 8.8.4.4")
    assert isinstance(out, CommandResult)
    query_anyipv4_result = json.loads(out.stdout)
    assert isinstance(query_anyipv4_result, dict)
    jsonschema.validate(instance=query_anyipv4_result, schema=get_query_result_schema())


def test_query_anyipv6(app):
    out = app.app_cmd("query anyipv6 2606:4700:4700::1111")
    assert isinstance(out, CommandResult)
    query_anyipv6_result = json.loads(out.stdout)
    assert isinstance(query_anyipv6_result, dict)
    jsonschema.validate(instance=query_anyipv6_result, schema=get_query_result_schema())


def test_query_cname(app):
    out = app.app_cmd("query cname silentpush.com")
    assert isinstance(out, CommandResult)
    query_cname_result = json.loads(out.stdout)
    assert isinstance(query_cname_result, dict)
    common_properties["ttl"] = {"type": "number"}
    jsonschema.validate(instance=query_cname_result, schema=get_query_result_schema())


def test_query_mx(app):
    out = app.app_cmd("query mx silentpush.com")
    assert isinstance(out, CommandResult)
    query_mx_result = json.loads(out.stdout)
    assert isinstance(query_mx_result, dict)
    query_mx_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "mxhash": {"type": "string"}
    }
    query_mx_result_schema = get_query_result_schema(query_mx_properties)
    jsonschema.validate(instance=query_mx_result, schema=query_mx_result_schema)


def test_query_ns(app):
    out = app.app_cmd("query ns silentpush.com")
    assert isinstance(out, CommandResult)
    query_ns_result = json.loads(out.stdout)
    assert isinstance(query_ns_result, dict)
    query_ns_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "nshash": {"type": "string"}
    }
    query_ns_result_schema = get_query_result_schema(query_ns_properties)
    jsonschema.validate(instance=query_ns_result, schema=query_ns_result_schema)


def test_query_ptr4(app):
    out = app.app_cmd("query ptr4 8.8.4.4")
    assert isinstance(out, CommandResult)
    query_ptr4_result = json.loads(out.stdout)
    assert isinstance(query_ptr4_result, dict)
    jsonschema.validate(instance=query_ptr4_result, schema=get_query_result_schema())


def test_query_ptr6(app):
    out = app.app_cmd("query ptr6 2606:4700:4700::1111")
    assert isinstance(out, CommandResult)
    query_ptr6_result = json.loads(out.stdout)
    assert isinstance(query_ptr6_result, dict)
    jsonschema.validate(instance=query_ptr6_result, schema=get_query_result_schema())


def test_query_soa(app):
    out = app.app_cmd("query soa silentpush.com")
    assert isinstance(out, CommandResult)
    query_soa_result = json.loads(out.stdout)
    assert isinstance(query_soa_result, dict)
    query_soa_properties = {
        **common_properties,
        "soahash": {"type": "string"}
    }
    query_soa_result_schema = get_query_result_schema(query_soa_properties)
    jsonschema.validate(instance=query_soa_result, schema=query_soa_result_schema)


def test_query_txt(app):
    out = app.app_cmd("query txt silentpush.com")
    assert isinstance(out, CommandResult)
    query_txt_result = json.loads(out.stdout)
    assert isinstance(query_txt_result, dict)
    query_txt_properties = {
        **common_properties,
        "txthash": {"type": "string"}
    }
    query_txt_result_schema = get_query_result_schema(query_txt_properties)
    jsonschema.validate(instance=query_txt_result, schema=query_txt_result_schema)

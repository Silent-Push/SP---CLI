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


def get_answer_result_schema(properties: dict = common_properties):
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


def test_answer_a(app):
    out = app.app_cmd("answer a 8.8.4.4")
    assert isinstance(out, CommandResult)
    answer_a_result = json.loads(out.stdout)
    assert isinstance(answer_a_result, dict)
    jsonschema.validate(instance=answer_a_result, schema=get_answer_result_schema())


def test_answer_aaaa(app):
    out = app.app_cmd("answer aaaa 2a00:1450:4001:827::200e")
    assert isinstance(out, CommandResult)
    answer_aaaa_result = json.loads(out.stdout)
    assert isinstance(answer_aaaa_result, dict)
    jsonschema.validate(instance=answer_aaaa_result, schema=get_answer_result_schema())


def test_answer_cname(app):
    out = app.app_cmd("answer cname forward.dnstool.net")
    assert isinstance(out, CommandResult)
    answer_cname_result = json.loads(out.stdout)
    assert isinstance(answer_cname_result, dict)
    common_properties["ttl"] = {"type": "number"}
    jsonschema.validate(instance=answer_cname_result, schema=get_answer_result_schema())


def test_answer_mx(app):
    out = app.app_cmd("answer mx aspmx.l.google.com")
    assert isinstance(out, CommandResult)
    answer_mx_result = json.loads(out.stdout)
    assert isinstance(answer_mx_result, dict)
    answer_mx_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "mxhash": {"type": "string"}
    }
    answer_mx_result_schema = get_answer_result_schema(answer_mx_properties)
    jsonschema.validate(instance=answer_mx_result, schema=answer_mx_result_schema)


def test_answer_mxhash(app):
    out = app.app_cmd("answer mxhash 945c2009446d8a78240b8d1f81f8ae44")
    assert isinstance(out, CommandResult)
    answer_mx_result = json.loads(out.stdout)
    assert isinstance(answer_mx_result, dict)
    answer_mx_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "mxhash": {"type": "string"}
    }
    answer_mx_result_schema = get_answer_result_schema(answer_mx_properties)
    jsonschema.validate(instance=answer_mx_result, schema=answer_mx_result_schema)


def test_answer_ns(app):
    out = app.app_cmd("answer ns vida.ns.cloudflare.com")
    assert isinstance(out, CommandResult)
    answer_ns_result = json.loads(out.stdout)
    assert isinstance(answer_ns_result, dict)
    answer_ns_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "nshash": {"type": "string"}
    }
    answer_ns_result_schema = get_answer_result_schema(answer_ns_properties)
    jsonschema.validate(instance=answer_ns_result, schema=answer_ns_result_schema)


def test_answer_nshash(app):
    out = app.app_cmd("answer nshash 900516f65c3289e7093a79c82d96cdb7")
    assert isinstance(out, CommandResult)
    answer_ns_result = json.loads(out.stdout)
    assert isinstance(answer_ns_result, dict)
    answer_ns_properties = {
        **common_properties,
        "ttl": {"type": "number"},
        "nshash": {"type": "string"}
    }
    answer_ns_result_schema = get_answer_result_schema(answer_ns_properties)
    jsonschema.validate(instance=answer_ns_result, schema=answer_ns_result_schema)


def test_answer_ptr4(app):
    out = app.app_cmd("answer ptr4 google.com")
    assert isinstance(out, CommandResult)
    answer_ptr4_result = json.loads(out.stdout)
    assert isinstance(answer_ptr4_result, dict)
    jsonschema.validate(instance=answer_ptr4_result, schema=get_answer_result_schema())


def test_answer_ptr6(app):
    out = app.app_cmd("answer ptr6 google.com")
    assert isinstance(out, CommandResult)
    answer_ptr6_result = json.loads(out.stdout)
    assert isinstance(answer_ptr6_result, dict)
    jsonschema.validate(instance=answer_ptr6_result, schema=get_answer_result_schema())


def test_answer_soa(app):
    out = app.app_cmd("answer soa jomax.net*20210725")
    assert isinstance(out, CommandResult)
    answer_soa_result = json.loads(out.stdout)
    assert isinstance(answer_soa_result, dict)
    answer_soa_properties = {
        **common_properties,
        "soahash": {"type": "string"}
    }
    answer_soa_result_schema = get_answer_result_schema(answer_soa_properties)
    jsonschema.validate(instance=answer_soa_result, schema=answer_soa_result_schema)


def test_answer_soahash(app):
    out = app.app_cmd("answer soahash 5834142715158611446")
    assert isinstance(out, CommandResult)
    answer_soa_result = json.loads(out.stdout)
    assert isinstance(answer_soa_result, dict)
    answer_soa_properties = {
        **common_properties,
        "soahash": {"type": "string"}
    }
    answer_soa_result_schema = get_answer_result_schema(answer_soa_properties)
    jsonschema.validate(instance=answer_soa_result, schema=answer_soa_result_schema)


def test_answer_txt(app):
    out = app.app_cmd("answer txt v=spf1 include:squarespace-mail.com ~all")
    assert isinstance(out, CommandResult)
    answer_txt_result = json.loads(out.stdout)
    assert isinstance(answer_txt_result, dict)
    answer_txt_properties = {
        **common_properties,
        "txthash": {"type": "string"}
    }
    answer_txt_result_schema = get_answer_result_schema(answer_txt_properties)
    jsonschema.validate(instance=answer_txt_result, schema=answer_txt_result_schema)


def test_answer_txthash(app):
    out = app.app_cmd("answer txthash 5907326045926790673")
    assert isinstance(out, CommandResult)
    answer_txt_result = json.loads(out.stdout)
    assert isinstance(answer_txt_result, dict)
    answer_txt_properties = {
        **common_properties,
        "txthash": {"type": "string"}
    }
    answer_txt_result_schema = get_answer_result_schema(answer_txt_properties)
    jsonschema.validate(instance=answer_txt_result, schema=answer_txt_result_schema)

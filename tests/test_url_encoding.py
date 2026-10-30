from unittest.mock import MagicMock, patch

from sp.common.utils import (
    encode_path_segment, encode_query_params, encode_query_value,
)
from tests.fixtures.app import app


def test_encode_path_segment_keeps_plain_iocs():
    assert encode_path_segment("ig.com") == "ig.com"
    assert encode_path_segment("1.2.3.4") == "1.2.3.4"
    assert encode_path_segment("2001:db8::1") == "2001:db8::1"
    assert encode_path_segment("*.ig.com") == "*.ig.com"


def test_encode_path_segment_escapes_url_syntax():
    assert encode_path_segment("ig.com/../x?a=1#b") == "ig.com%2F..%2Fx%3Fa%3D1%23b"


def test_encode_query_value_escapes_separators():
    assert encode_query_value("ig.com&format=csv") == "ig.com%26format%3Dcsv"


def test_encode_query_params():
    assert encode_query_params(["limit=2", "sort=last_seen/-"]) == "limit=2&sort=last_seen%2F-"
    assert encode_query_params(["q=a&b=c"]) == "q=a%26b%3Dc"
    assert encode_query_params(["flag"]) == "flag="


def test_threatcheck_url_is_encoded(app):
    response = MagicMock(status_code=200, content=b'{"listed_details": [{}]}')
    with patch("sp.commands.base.threatcheck.requests.get", return_value=response) as get:
        app.app_cmd("threatcheck ig.com")
    url = get.call_args[0][0]
    assert "query=ig.com&" in url
    assert "data_source=iofa&query_type=name&" in url

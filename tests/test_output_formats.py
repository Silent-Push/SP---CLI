from unittest.mock import MagicMock, patch

from sp.commands.base.BaseCommand import BaseCommand
from tests.fixtures.app import API_REQUEST


def test_csv_rows_quote_values():
    rows = BaseCommand._to_rows({"a": 1, "b": "x, y", "c": None}, ",")
    assert rows.splitlines()[:3] == ["a,1", 'b,"x, y"', "c,"]


def test_tsv_rows_use_real_tabs():
    assert BaseCommand._to_rows({"a": 1, "bb": 2}, "\t").splitlines()[:2] == ["a\t1", "bb\t2"]


def test_single_values_stay_as_they_are():
    assert BaseCommand._to_rows(35, ",") == 35
    assert BaseCommand._to_rows("no listing", "\t") == "no listing"


def test_aligned_rows_line_up_values():
    rows = BaseCommand._to_aligned_rows({"a": 1, "bbb": None, "cc": "x y"}).splitlines()
    assert rows[:3] == ["a    1", "bbb  ", "cc   x y"]


def test_aligned_rows_keep_single_values():
    assert BaseCommand._to_aligned_rows(35) == 35


def test_tsv_is_aligned_only_in_a_terminal(app):
    response = MagicMock(status_code=200, content=b'{"response": {"a": 1, "bbb": 2}}')
    with patch(API_REQUEST, return_value=response):
        assert "bbb\t2" in app.app_cmd("score ig.com -v -t").stdout
        with patch("cmd2.utils.StdSim.isatty", return_value=True):
            assert "bbb  2" in app.app_cmd("score ig.com -v -t").stdout

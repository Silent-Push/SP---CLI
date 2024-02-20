import argparse
from typing import Optional, Sequence, Type

from cmd2 import Cmd2ArgumentParser
from cmd2.argparse_custom import Cmd2HelpFormatter


baseCmd2ArgumentParser = Cmd2ArgumentParser()
baseCmd2ArgumentParser.add_argument(
    "--json",
    help="Output as JSON"
)
baseCmd2ArgumentParser.add_argument(
    "--csv",
    help="Output as CSV"
)
from cmd2 import Statement, with_default_category, with_argparser

from sp.commands.base.spql import WebScan, FeedScan
from sp.commands.base.BaseCommandSet import BaseCommandSet


@with_default_category("SPQL")
class SPQLCommandSet(BaseCommandSet):
    """
    SPQL Command Set:
         - **webscan**: sub command of spql command
         - **feedscan**: sub command of spql command
         - ... (more to come)
    """

    webscan_parser = BaseCommandSet._get_webscan_arg_parser()
    """The argument parser for the SPQL command"""

    @with_argparser(webscan_parser, preserve_quotes=True)
    def do_webscan(self, params: Statement):
        """
        SPQL Webscan

        :param params: The passed command parameters
        :return: None
        """
        with WebScan(params, self) as spql:
            spql.scan()

    feedscan_parser = BaseCommandSet._get_feedscan_arg_parser()
    @with_argparser(feedscan_parser, preserve_quotes=True)
    def do_feedscan(self, params: Statement):
        """
        SPQL Feedscan

        :param params: The passed command parameters
        :return: None
        """
        with FeedScan(params, self) as spql:
            spql.scan()

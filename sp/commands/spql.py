from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.spql import FeedScan, WebScan


@with_default_category("SPQL")
class SPQLCommandSet(BaseCommandSet):
    """
    SPQL Command Set:
         - **websearch**: sub command of spql command
         - **feedsearch**: sub command of spql command
         - ... (more to come)
    """

    websearch_parser = BaseCommandSet._get_websearch_arg_parser()
    """The argument parser for the SPQL command"""

    @with_argparser(websearch_parser, preserve_quotes=True)
    def do_websearch(self, params: Statement):
        """
        SPQL Websearch

        :param params: The passed command parameters
        :return: None
        """
        with WebScan(params, self) as spql:
            spql.scan()

    feedsearch_parser = BaseCommandSet._get_feedsearch_arg_parser()

    @with_argparser(feedsearch_parser, preserve_quotes=True)
    def do_feedsearch(self, params: Statement):
        """
        SPQL Feedsearch

        :param params: The passed command parameters
        :return: None
        """
        with FeedScan(params, self) as spql:
            spql.scan()

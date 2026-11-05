from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.whois import WhoisLive


@with_default_category("Whois")
class WhoisCommandSet(BaseCommandSet):
    """
    Whois Command Set
    """

    whois_parser = BaseCommandSet._get_domain_arg_parser()
    """The argument parser for the whois command"""

    @with_argparser(whois_parser)
    def do_whoislive(self, params: Statement):
        """
        Search real-time whois information for domain

        :param params: The passed command parameters
        :return: None
        """
        with WhoisLive(params, self) as whoislive:
            whoislive.search()

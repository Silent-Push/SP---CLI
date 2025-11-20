from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.threatcheck import ThreatCheck, BulkThreatCheck
from sp.common.parse_ioc import IOCUtils


@with_default_category("ThreatCheck")
class ThreatCheckCommandSet(BaseCommandSet):
    """
    Threat Check Command Set
    """

    threatcheck_parser = BaseCommandSet._get_threatcheck_arg_parser()
    """The argument parser for the threatcheck command"""

    @with_argparser(threatcheck_parser)
    def do_threatcheck(self, params: Statement):
        """
        Threat Check a single name or IP

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with ThreatCheck(params, self) as threatcheck:
            threatcheck.check()

    bulk_threatcheck_parser = BaseCommandSet._get_bulk_threatcheck_arg_parser()
    """The argument parser for the bulk_threatcheck command"""

    @with_argparser(bulk_threatcheck_parser)
    def do_bulk_threatcheck(self, params: Statement):
        """
        | Threat Check domains or IPs (ipv4 or ipv6) in a bulk
        | You can also use a file as input, i.e.:
        |   ``cat to_threatcheck.txt | xargs sp bulk_threatcheck``

        :param params: The passed command parameters
        :return: None
        """
        with BulkThreatCheck(params, self) as bulk_threatcheck:
            bulk_threatcheck.check()

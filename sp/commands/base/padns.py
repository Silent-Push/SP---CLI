import json

import requests
from cmd2 import CommandSet, Statement

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_KEY, API_URL


class BasePADNS(BaseCommand):
    def lookup(self):
        """
        The PADNS main command logic

        :return: None
        """
        if not self._params.ioc:
            self._commandSet._cmd.perror("You need to pass the IoC")
            return
        self._response = requests.get(
            self._URL,
            headers={"x-api-key": API_KEY, "User-Agent": "SP-CLI"},
        )
        self.check_error()
        try:
            self._response = json.loads(self._response.content).get("response")
        except json.JSONDecodeError as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e.msg}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The logic after executing the command

        :param exc_type: Exception type, if need to catch
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)


class PADNSLookup(BasePADNS):
    """
    PADNS Lookup main command
    """

    _URL = (
            API_URL + "v1/merge-api/explore/padns/lookup/{type}/{qtype}/{ioc}/?format=json"
    )
    """The PADNS endpoint URL"""
    _type: str = "query"
    """The type of the PADNS query"""
    _qtype: str = "any"
    """The sub type of the query"""

    def __init__(
        self,
        params: Statement,
        command_set: CommandSet,
        type: str = "query",
        qtype: str = "any",
    ):
        """
        Context manager class for the PADNS sub commands,
        it's used by the sub commands i.e.: query

        :param params: The passed command options
        :param command_set: The CommandSet object related to the command
        :param type: A PADNS query type, i.e.: query
        :param qtype: The sub type of the query, i.e.: any
        """
        self._type = type
        self._qtype = qtype
        super().__init__(params, command_set)

    def __enter__(self):
        """
        The logic before executing the command

        :return: PADNS
        """
        self._URL = self._URL.format(
            type=self._type, qtype=self._qtype, ioc=self._params.ioc
        )
        super().__enter__()
        # self._feedback = f"{self._URL[self._URL.index('lookup/') + 7:]}"
        return self


class PADNSSearch(BasePADNS):
    """
    PADNS Search main command
    """

    _URL = API_URL + "v1/merge-api/explore/padns/search/{type}{qtype}/?format=json"
    """The PADNS endpoint URL"""
    _type: str = "ipdiversity"
    """The type of the PADNS query"""
    _qtype: str = ""
    """The sub type of the query"""

    def __init__(
        self,
        params: Statement,
        command_set: CommandSet,
        type: str = "ipdiversity",
        qtype: str = "",
    ):
        """
        Context manager class for the PADNS sub commands,
        it's used by the sub commands i.e.: query

        :param params: The passed command options
        :param command_set: The CommandSet object related to the command
        :param type: A PADNS search type, i.e.: ipdiversity
        :param qtype: The sub type of the search, i.e.: ns
        """
        self._type = type
        self._qtype = qtype
        super().__init__(params, command_set)

    def lookup(self):
        super().lookup()
        self._response = self._response.get("records")

    def __enter__(self):
        """
        The logic before executing the command

        :return: PADNS
        """
        qtype = f"/{self._qtype}" if self._qtype else ""
        self._URL = self._URL.format(type=self._type, qtype=qtype)
        self._URL += f"&domain={self._params.ioc}"
        super().__enter__()
        # self._feedback = f"{self._URL[self._URL.index('search/') + 7:]}"
        return self

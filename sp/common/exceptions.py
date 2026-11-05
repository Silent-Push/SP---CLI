import json
import re


class CommandError(Exception):
    """
    Stops a command and shows the user a plain message, no traceback

    Raise it from anywhere inside a command, BaseCmdApp.pexcept calls show()
    """

    def show(self, cmd) -> None:
        """
        Shows the error to the user, override it to change how the error is presented

        :param cmd: The cmd2 app
        :return: None
        """
        cmd.perror(str(self))


class ResponseParseError(CommandError):
    """The API answered, but not with what the command expected"""

    def __init__(self, cause: Exception):
        super().__init__(f"Can't parse command response: {cause}")


class ApiTimeoutError(CommandError):
    """The API took longer than settings.API_TIMEOUT to answer"""

    def __init__(self, timeout: float):
        super().__init__(f"The Silent Push API didn't answer in {timeout:g}s, try again later")


class ApiConnectionError(CommandError):
    """The API couldn't be reached at all, i.e.: no network, SSL or proxy problems"""

    def __init__(self, cause: Exception):
        super().__init__(f"Can't reach the Silent Push API: {cause.__class__.__name__}")


class ApiError(CommandError):
    """The API answered with an error status"""

    def __init__(self, response):
        """
        :param response: The API response, any status other than 200
        """
        self.status = response.status_code
        self.retry_after = response.headers.get("Retry-After")
        super().__init__(self._get_detail(response))

    @staticmethod
    def _get_detail(response) -> str:
        """
        Tries to extract as much error from the response payload as possible

        :param response: The API response
        :return: The error, JSON errors or the body of an HTML page
        """
        content = response.content.decode(errors="replace")
        try:
            error = str(json.loads(content).get("errors", content))
        except (json.JSONDecodeError, AttributeError):
            body = content.find("<body")
            error = re.sub("<.*?>|\n", " ", content[body:] if body >= 0 else content)
        return re.sub(" +", " ", error).strip()

    @property
    def hint(self) -> str:
        """What the user can do about the error"""
        if self.status in (401, 403):
            return "Is your API key correct?"
        if self.status == 404:
            return "Not found, check the IoC or the command options"
        if self.status == 429:
            when = f"in {self.retry_after}s" if self.retry_after else "later"
            return f"Rate limited, try again {when}"
        if self.status >= 500:
            return "The Silent Push API is having problems, try again later"
        return "Check the command options, try 'help <command>'"

    def show(self, cmd) -> None:
        """
        Overrides CommandError.show: shows the status line and what the user can do about it

        :param cmd: The cmd2 app
        :return: None
        """
        cmd.perror("Something went wrong :(")
        cmd.perror(f"Status Code {self.status}: {str(self)[:100]}...")
        cmd.pwarning(self.hint)


class JobPending(CommandError):
    """Long running tasks return a job instead of the result, not a failure so `sp` still exits with 0"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        super().__init__(f"This command is taking too long, try again later using the command: `job {job_id}`")

    def show(self, cmd) -> None:
        """
        Overrides CommandError.show: a warning, so `sp` exits with 0

        :param cmd: The cmd2 app
        :return: None
        """
        cmd.pwarning(str(self))

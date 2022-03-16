from typing import Callable, Any, List, Dict
from pathlib import Path

from telethon.tl.custom.dialog import Dialog

from telegramcleaner.interactive.stream import Stream
from telegramcleaner.interactive.requests.parsers import (
    parse_session_name,
    parse_api_id,
    parse_api_hash,
    parse_group_numbers
)
from telegramcleaner import errors


SENTINEL = object()
DEFAULT_SESSION_NAME = "telegram"


def _get_group_lines(groups: Dict[int, Dialog]) -> List[str]:
    lines = []
    for number, group in groups.items():
        line = "[{number}] {title}".format(number=number, title=group.title)
        lines.append(line)

    return lines


class Requester:

    def __init__(self, stream: Stream):
        self._stream = stream

    def request_session_path(self) -> Path:
        string = self._request(
            prompt_text=("Enter a name or a path of a session file"
                         f"(default is «{DEFAULT_SESSION_NAME}»:"),
            parser=parse_session_name,
            default=DEFAULT_SESSION_NAME
        )
        path = Path(string).absolute()

        return path

    def request_api_id(self) -> int:
        return self._request(
            prompt_text="Enter an app_id:",
            parser=parse_api_id
        )

    def request_api_hash(self) -> str:
        return self._request(
            prompt_text="Enter an api_hash:",
            parser=parse_api_hash
        )

    def request_groups_for_clearing(self, groups: List[Dialog]) -> List[Dialog]:
        numbered_groups = {number: group for number, group in enumerate(groups, start=1)}
        group_numbers = self._request(
            prompt_text=("Select groups to delete messages:\n" +
                         "\n".join(_get_group_lines(numbered_groups)) +
                         "\nEnter group numbers separated by a space (for example: 1 2 5 27)"),
            parser=parse_group_numbers
        )
        groups = [numbered_groups[i] for i in group_numbers]

        return groups

    def _request(self, prompt_text: str, parser: Callable[[str], Any],
                 default: object = SENTINEL) -> Any:
        self._stream.output(prompt_text)

        while True:
            text = self._stream.input()
            if not text and default is not SENTINEL:
                return default

            try:
                return parser(text)
            except errors.ParsingError:
                self._stream.output("Invalid input! Try again!\n")

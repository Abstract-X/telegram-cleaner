from typing import List
from string import ascii_lowercase, digits

from telegramcleaner import errors


def parse_session_name(text: str) -> str:
    if not text:
        raise errors.ParsingError()

    return text


def parse_api_id(text: str) -> int:
    try:
        return int(text)
    except ValueError:
        raise errors.ParsingError()


def parse_api_hash(text: str) -> str:
    if (len(text) != 32) or any(i not in ascii_lowercase + digits for i in text):
        raise errors.ParsingError()

    return text


def parse_group_numbers(text: str) -> List[int]:
    return [int(i) for i in text.split(" ") if i]

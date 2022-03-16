import contextlib

from telethon.sync import TelegramClient

from telegramcleaner.interactive.stream import Stream
from telegramcleaner.interactive.requests.requester import Requester
from telegramcleaner.utils.telegram import (
    get_groups,
    get_message_ids_from_group,
    delete_messages_in_group
)


def main():
    stream = Stream()
    requester = Requester(stream)

    session_path = requester.request_session_path()
    api_id = requester.request_api_id()
    api_hash = requester.request_api_hash()

    with TelegramClient(str(session_path), api_id, api_hash) as client:
        groups = get_groups(client, stream)
        if groups:
            groups = requester.request_groups_for_clearing(groups)
            for group in groups:
                message_ids = get_message_ids_from_group(client, group, stream)
                delete_messages_in_group(client, group, message_ids, stream)


if __name__ == "__main__":
    with contextlib.suppress(KeyboardInterrupt):
        main()

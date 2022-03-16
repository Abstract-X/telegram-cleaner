from typing import List
import time

from telethon.sync import TelegramClient
from telethon.tl.custom.dialog import Dialog
from telethon.tl.patched import MessageService

from telegramcleaner.interactive.stream import Stream


def get_groups(client: TelegramClient, stream: Stream) -> List[Dialog]:
    groups = []
    stream.output_renewable_line("Requesting groups...")
    for i in client.iter_dialogs(ignore_migrated=True):
        if i.is_group:
            groups.append(i)
            stream.output_renewable_line(f"Requesting groups [{len(groups)}]...")

    if groups:
        end_line_text = f"Groups received [{len(groups)}]!"
    else:
        end_line_text = "You don't have groups!"
    stream.output_renewable_line_end(end_line_text)

    return groups


def get_message_ids_from_group(client: TelegramClient,
                               group: Dialog, stream: Stream) -> List[int]:
    message_ids = []
    stream.output_renewable_line(f"Requesting messages from the group «{group.title}»...")
    for i in client.iter_messages(group.input_entity, wait_time=3, from_user="me"):
        if type(i) != MessageService:
            message_ids.append(i.id)
            stream.output_renewable_line(f"Requesting messages from the group "
                                         f"«{group.title}» [{len(message_ids)}]...")

    if message_ids:
        end_line_text = f"Messages from the «{group.title}» group received [{len(message_ids)}]!"
    else:
        end_line_text = f"Your messages in the «{group.title}» group were not found!"
    stream.output_renewable_line_end(end_line_text)

    return message_ids


def _cut_list(list_: list, quantity: int) -> List[list]:
    parts = []
    if list_:
        start_index = 0
        end_index = quantity
        while start_index <= len(list_) - 1:
            parts.append(list_[start_index:end_index])
            start_index += quantity
            end_index += quantity

    return parts


def delete_messages_in_group(client: TelegramClient, group: Dialog,
                             message_ids: List[int], stream: Stream) -> None:
    if not message_ids:
        return

    deleted_count = 0
    stream.output_renewable_line(f"Deleting messages from the «{group.title}» group...")
    for chunk in _cut_list(message_ids, 100):
        client.delete_messages(group.input_entity, chunk)
        deleted_count += len(chunk)
        stream.output_renewable_line(f"Deleting messages from the «{group.title}» group "
                                     f"[{deleted_count}/{len(message_ids)}]...")
        time.sleep(3)

    stream.output_renewable_line_end(f"Messages from the «{group.title}» group "
                                     f"have been deleted [{deleted_count}]!")

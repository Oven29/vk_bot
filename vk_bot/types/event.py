from typing import Dict, List, Any

from ..enums import TypeEvent


class Event:
    """
        Represents a VK event.
        Docs: https://dev.vk.com/ru/api/user-long-poll/getting-started?ref=old_portal#
    """
    def __init__(self, event: List[Any]) -> None:
        # Initialize common fields to None
        self.peer_id = None
        self.timestamp = None
        self.extra_fields = None
        self.message_id = None

        # Determine the event type
        self.type = TypeEvent(event[0])
        print(event)

        if self.type == TypeEvent.MESSAGE_FLAGS_REPLACE:
            self.message_id = event[1]
            self.flags = event[2]
            self.unpack_message_extra_field(event[3:])

        elif self.type == TypeEvent.MESSAGE_FLAGS_SET:
            self.message_id = event[1]
            self.mask = event[2]
            self.unpack_message_extra_field(event[3:])

        elif self.type == TypeEvent.MESSAGE_FLAGS_RESET:
            self.message_id = event[1]
            self.mask = event[2]
            self.unpack_message_extra_field(event[3:])

        elif self.type == TypeEvent.NEW_MESSAGE:
            self.message_id = event[1]
            self.flags = event[2]
            # self.minor_id = event[3]
            self.unpack_message_extra_field(event[3:])

        elif self.type == TypeEvent.MESSAGE_EDIT:
            self.message_id = event[1]
            self.mask = event[2]
            self.peer_id = event[3]
            self.timestamp = event[4]
            self.text = event[5]  # Renamed to text for consistency
            self.attachments = event[6]

        elif self.type == TypeEvent.MESSAGE_READ_INCOMING:
            self.peer_id = event[1]
            self.local_id = event[2]

        elif self.type == TypeEvent.MESSAGE_READ_OUTGOING:
            self.peer_id = event[1]
            self.local_id = event[2]

        elif self.type == TypeEvent.FRIEND_ONLINE:
            self.user_id = -event[1]
            self.extra = event[2]
            self.timestamp = event[3]

        elif self.type == TypeEvent.FRIEND_OFFLINE:
            self.user_id = -event[1]
            self.flags = event[2]
            self.timestamp = event[3]

        elif self.type == TypeEvent.PEER_FLAGS_RESET:
            self.peer_id = event[1]
            self.mask = event[2]

        elif self.type == TypeEvent.PEER_FLAGS_REPLACE:
            self.peer_id = event[1]
            self.flags = event[2]

        elif self.type == TypeEvent.PEER_FLAGS_SET:
            self.peer_id = event[1]
            self.mask = event[2]

        elif self.type == TypeEvent.MESSAGES_DELETE:
            self.peer_id = event[1]
            self.local_id = event[2]

        elif self.type == TypeEvent.MESSAGES_RESTORE:
            self.peer_id = event[1]
            self.local_id = event[2]

        elif self.type == TypeEvent.MAJOR_ID_UPDATE:
            self.peer_id = event[1]
            self.major_id = event[2]

        elif self.type == TypeEvent.MINOR_ID_UPDATE:
            self.peer_id = event[1]
            self.minor_id = event[2]

        elif self.type == TypeEvent.CHAT_SETTINGS_UPDATE:
            self.chat_id = event[1]
            self.self_updated = event[2]

        elif self.type == TypeEvent.CHAT_INFO_UPDATE:
            self.type_id = event[1]
            self.peer_id = event[2]
            self.info = event[3]

        elif self.type == TypeEvent.USER_TYPING_DIALOG:
            self.user_id = event[1]
            self.flags = event[2]

        elif self.type == TypeEvent.USER_TYPING_CHAT:
            self.user_id = event[1]
            self.chat_id = event[2]

        elif self.type == TypeEvent.USERS_TYPING_CHAT:
            self.user_ids = event[1]
            self.peer_id = event[2]
            self.total_count = event[3]
            self.timestamp = event[4]

        elif self.type == TypeEvent.USERS_RECORDING_AUDIO:
            self.user_ids = event[1]
            self.peer_id = event[2]
            self.total_count = event[3]
            self.timestamp = event[4]

        elif self.type == TypeEvent.USER_CALL:
            self.user_id = event[1]
            self.call_id = event[2]

        elif self.type == TypeEvent.COUNTER_UPDATE:
            self.count = event[1]

        elif self.type == TypeEvent.NOTIFICATIONS_SETTINGS_UPDATE:
            self.peer_id = event[1]
            self.sound = event[2]
            self.disabled_until = event[3]

        else:
            # Store any unhandled fields in extra_fields
            self.extra_fields = event[1:]

    def unpack_message_extra_field(self, fields: List[Any]) -> None:
        if fields:
            self.peer_id = fields.pop(0)
        if fields:
            self.timestamp = fields.pop(0)
        if fields:
            self.text = fields.pop(0)
        if fields:
            self.attachments = fields.pop(0)
        if fields:
            self.random_id = fields.pop(0)

    def __dict__(self) -> Dict[str, Any]:
        return dict(
            type=self.type,
            peer_id=self.peer_id,
            timestamp=self.timestamp,
            message_id=self.message_id,
        )

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.__dict__()!r})'

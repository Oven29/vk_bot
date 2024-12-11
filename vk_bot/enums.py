from enum import Enum


class TypeEvent(int, Enum):
    """Docs: https://dev.vk.com/ru/api/user-long-poll/getting-started?ref=old_portal#"""
    MESSAGE_FLAGS_REPLACE = 1
    MESSAGE_FLAGS_SET = 2
    MESSAGE_FLAGS_RESET = 3
    NEW_MESSAGE = 4
    MESSAGE_EDIT = 5
    MESSAGE_READ_INCOMING = 6
    MESSAGE_READ_OUTGOING = 7
    FRIEND_ONLINE = 8
    FRIEND_OFFLINE = 9
    PEER_FLAGS_RESET = 10
    PEER_FLAGS_REPLACE = 11
    PEER_FLAGS_SET = 12
    MESSAGES_DELETE = 13
    MESSAGES_RESTORE = 14
    MAJOR_ID_UPDATE = 20
    MINOR_ID_UPDATE = 21
    CHAT_SETTINGS_UPDATE = 51
    CHAT_INFO_UPDATE = 52
    USER_TYPING_DIALOG = 61
    USER_TYPING_CHAT = 62
    USERS_TYPING_CHAT = 63
    USERS_RECORDING_AUDIO = 64
    USER_CALL = 70
    COUNTER_UPDATE = 80
    NOTIFICATIONS_SETTINGS_UPDATE = 114


class ButtonColor(str, Enum):
    """Docs: https://dev.vk.com/ru/api/bots/development/keyboard"""
    PRIMARY = "primary"  # Main action button
    SECONDARY = "secondary"  # Regular button
    NEGATIVE = "negative"  # Dangerous actions like delete
    POSITIVE = "positive"  # Confirmation actions like agree


class ButtonType(str, Enum):
    """Docs: https://dev.vk.com/ru/api/bots/development/keyboard"""
    TEXT = "text"  # Sends a message with predefined text
    LOCATION = "location"  # Opens a dialog to share location
    VKPAY = "vkpay"  # Opens VK Pay payment window
    OPEN_LINK = "open_link"  # Opens a specified link
    OPEN_APP = "open_app"  # Opens a mini-app or game
    CALLBACK = "callback"  # Sends a callback event to the bot

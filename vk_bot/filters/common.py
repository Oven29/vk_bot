from typing import Optional

from . import BaseFilter
from ..enums import TypeEvent
from ..types import Event


class TypeFilter(BaseFilter):
    """Filter events by type."""
    def __init__(self, *types: TypeEvent) -> None:
        self.types = types

    async def __call__(self, event: Event) -> bool:
        return event.type in self.types


class MessageFilter(TypeFilter):
    """Filter events by message type."""
    def __init__(self, *texts: str, ignore_case: bool = True) -> None:
        self.ignore_case = ignore_case
        if self.ignore_case:
            self.texts = [text.lower() for text in texts]
        else:
            self.texts = texts
        super().__init__(TypeEvent.NEW_MESSAGE)

    async def __call__(self, event: Event) -> bool:
        if not await super().__call__(event):
            return False

        if not event.text:
            return False

        if len(self.texts) == 0:
            pass

        if (self.ignore_case and event.text.lower() in self.texts) or event.text in self.texts:
            return True

        return False


class StateFilter(BaseFilter):
    """Filter events by user state."""

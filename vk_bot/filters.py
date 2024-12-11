from abc import ABC, abstractmethod
from typing import Optional

from .enums import TypeEvent
from .types.event import Event


class BaseFilter(ABC):
    @abstractmethod
    async def __call__(self, event: Event) -> bool:
        """Check if the event passes the filter.

        Args:
            event (Event): The event to check.

        Returns:
            bool: True if the event passes the filter, False otherwise.
        """
        raise NotImplementedError


class TypeFilter(BaseFilter):
    """Filter events by type."""
    def __init__(self, *types: TypeEvent) -> None:
        self.types = types

    async def __call__(self, event: Event) -> bool:
        return event.type in self.types


class MessageFilter(TypeFilter):
    """Filter events by message type."""
    def __init__(self, text: Optional[str] = None, ignore_case: bool = True) -> None:
        self.ignore_case = ignore_case
        self.text = text.lower() if self.ignore_case and text else text
        super().__init__(TypeEvent.NEW_MESSAGE)

    async def __call__(self, event: Event) -> bool:
        if not await super().__call__(event):
            return False

        if self.text is None or (self.ignore_case and event.text.lower() == self.text) or event.text == self.text:
            return True

        return False

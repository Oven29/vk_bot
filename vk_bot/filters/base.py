from abc import ABC, abstractmethod

from ..enums import TypeEvent
from ..types import Event


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

import logging
from typing import Any, Callable, List, Tuple
from aiovk import API

from .filters import BaseFilter
from .types import Event


HandlerType = Callable[[Event, API], Tuple[int] | int | None]


class Router:
    def __init__(self, name: str | None = None) -> None:
        """
        Initialize the Router.

        Args:
            name (str, optional): The name of the router. Defaults to 'root'.
        """
        self.handlers: List[HandlerType] = []
        self.common_filters: List[BaseFilter] = []
        self.name = name or 'root'
        self.logger = logging.getLogger(f'{__name__}:{self.name}')
        self.dp = None

    def __call__(self, *filters: BaseFilter) -> Callable[[HandlerType], HandlerType]:
        """
        Decorator to register a handler with optional filters.
        Handler must returns message_id or tuple of message_ids to send

        Args:
            filters (BaseFilter): Filters to apply to the handler.

        Returns:
            Callable[[HandlerType], HandlerType]: Decorated handler with applied filters.

        Example:
            @router(filter1, filter2)
            def my_handler(event, vk) -> int:
                pass
        """
        def decorator(func: HandlerType) -> HandlerType:
            self.register_handler(func, *filters)
            return func

        return decorator

    def register_handler(self, handler: HandlerType, *filters: BaseFilter) -> None:
        """
        Register a handler with optional filters.

        Args:
            handler (HandlerType): The handler function to register.
            filters (BaseFilter): Filters to apply to the handler.
        """
        self.handlers.append((handler, filters))

    def filter(self, *filters: BaseFilter) -> None:
        """
        Add filters to the router's common filters.

        Args:
            filters (BaseFilter): Filters to add to the common filters.
        """
        self.common_filters.extend(filters)

    def _set_dp(self, dp: Any) -> None:
        """
        Set the dispatcher for the router.

        Args:
            dp (Dispatcher): The dispatcher to set.
        """
        self.dp = dp

    async def handle_event(self, event: Event, api: API) -> bool:
        """
        Handle an event by iterating over registered handlers and applying filters.

        Args:
            event (Event): The event to handle.
            api (API): The VK API method object.

        Returns:
            bool: True if the event was handled, False otherwise.
        """
        async def check(*filters: BaseFilter) -> bool:
            for f in filters:
                if not await f(event):
                    return False

            return True

        for handler, filters in self.handlers:
            if (await check(*self.common_filters, *filters)):
                self.logger.info(f'Handling {event} with handler {handler.__name__}')
                res = await handler(event, api)

                if res is None:
                    self.logger.warning('Dp instaince is None')
                    return True
                if isinstance(res, int):
                    messages = [res]
                else:
                    messages = res

                if self.dp is not None:
                    self.dp.add_senging_message(*messages)

                return True

        return False

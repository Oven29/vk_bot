import logging
from typing import Callable, List, Optional, Tuple
from aiovk import TokenSession, API, LongPoll

from .filters import BaseFilter
from .storage import BaseStorage
from .types import Event
from .router import Router, HandlerType


class Dispatcher:
    """
      Class for handling events from vk.com
    """
    def __init__(self, token: str, storage: Optional[BaseStorage] = None) -> None:
        """
        Initialize the Dispatcher with a token.

        Args:
            token: The token for the vk.com API.
        """
        self.__token = token
        self.__dispatcher_router = Router('dispatcher')
        self.register_handler = self.__dispatcher_router.register_handler
        self.handler = self.__dispatcher_router.__call__
        self.__routers: List[Router] = [self.__dispatcher_router]
        self.__logger = logging.getLogger(__name__)
        self.__sending_messages = []
        self.__storage = storage

    def include_routers(self, *routers: Tuple[Router]) -> None:
        """
        Include one or more routers to handle events.

        Args:
            *routers: One or more routers to include.
        """
        for router in routers:
            router._set_dp(self)
            self.__logger.info(f'Registering router {router.name}')
            self.__routers.append(router)

    def add_senging_message(self, *message_ids: int) -> None:
        """
        Add a message to the list of messages that are being sent.

        Args:
            *message_id (int): The ID of the message being sent.
        """
        self.__sending_messages.extend(message_ids)

    async def start_polling(
        self,
        startup: Optional[Callable] = None,
        shutdown: Optional[Callable] = None,
    ) -> None:
        """
        Start listening to events from vk.com

        Args:
            startup: A function to call when the dispatcher starts.
            shutdown: A function to call when the dispatcher is shutting down.
        """
        try:
            async with TokenSession(access_token=self.__token) as vk_session:
                self.__logger.info('Starting VK LongPoll listener...')
                api = API(vk_session)

                if startup is not None:
                    await startup(api)

                longpoll = LongPoll(api, mode=2)

                async for ev in longpoll.iter():
                    event = Event(ev)
                    self.__logger.info(f'New {event}')

                    if event.message_id in self.__sending_messages:
                        self.__sending_messages.remove(event.message_id)
                        continue

                    try:
                        for router in self.__routers:
                            if await router.handle_event(event, api):
                                break
                        else:
                            self.__logger.info(f'{event} was not handled')

                    except Exception as e:
                        self.__logger.error(e, exc_info=True)

        except KeyboardInterrupt:
            self.__logger.info('Dispatcher stopped')

        finally:
            self.__logger.info('Shutting down the VK LongPoll listener.')
            if shutdown is not None:
                await shutdown(api)

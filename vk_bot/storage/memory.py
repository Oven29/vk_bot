from typing import Any

from .base import BaseStorage


class MemoryStorage(BaseStorage):
    def __init__(self):
        self.__storage = {}

    async def get(self, key: Any) -> Any:
        return self.__storage.get(key)

    async def set(self, key: Any, value: Any) -> None:
        self.__storage[key] = value

    async def delete(self, key: Any) -> None:
        del self.__storage[key]

"""
Misc utilities shared throughout the library.
"""
import datetime

import collections
import typing


class AsyncIteratorWrapper(collections.AsyncIterator):
    """
    Wraps a function so that it can be iterated over asynchronously.
    """

    def __init__(self, client, coro: collections.Coroutine):
        self.client = client
        self.coro = coro

        self.items = collections.deque()

        self._filled = False

    async def _fill(self):
        self.items.extend(await self.coro)
        self._filled = True

    async def __anext__(self):
        if not self._filled:
            await self._fill()

        try:
            return self.items.popleft()
        except IndexError:
            raise StopAsyncIteration


def to_datetime(timestamp: str) -> datetime.datetime:
    """
    Converts a Discord-formatted timestamp to a datetime object.

    :param timestamp: The timestamp to convert.
    :return: The :class:`datetime.datetime` object that corresponds to this datetime.
    """
    if timestamp is None:
        return

    if timestamp.endswith("+00:00"):
        return datetime.datetime.strptime(timestamp[:-6], "%Y-%m-%dT%H:%M:%S.%f")
    else:
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f")
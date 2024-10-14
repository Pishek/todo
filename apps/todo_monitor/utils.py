import asyncio
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import TypeVar

from typing_extensions import ParamSpec

T = TypeVar("T")
P = ParamSpec("P")  # noqa: VNE001


def coro(func: Callable[P, Awaitable[T]]) -> Callable[P, T]:
    """
    Make it possible to run async code in sync context
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        async def async_wrapper(*args_: P.args, **kwargs_: P.kwargs) -> T:
            return await func(*args_, **kwargs_)

        return asyncio.get_event_loop().run_until_complete(async_wrapper(*args, **kwargs))

    return wrapper

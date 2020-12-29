import asyncio
import functools
from typing import Any, Callable, List, Tuple

from easy_notifyer.env import Env


def get_telegram_creds() -> Tuple[str, List[int]]:
    """
    Get telegram creds from environment variable
    Returns:
        Tuple[token(str), List[chat_id(int), ...]]
    """
    token = Env.EASY_NOTIFYER_TELEGRAM_TOKEN
    chat_id = Env.EASY_NOTIFYER_TELEGRAM_CHAT_ID
    error = EnvironmentError(f"Telegram token or chat_id is not found. token={token}, "
                             f"chat_id={chat_id}")
    if token is None or chat_id is None:
        raise error
    try:
        chat_id = [i.strip() for i in chat_id.split(',')]
        chat_id = [int(i) for i in chat_id if i]
    except ValueError as exc:
        raise error from exc
    return token, chat_id


async def run_sync(func: Callable, *args, **kwargs) -> Any:
    """
    Run sync func in async code in thread pool.
    Args:
        func(callable): func to run
        *args:
        **kwargs:
    Returns:
        same as func
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

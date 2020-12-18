import asyncio
import functools
from typing import Callable, List, Tuple, Union

from easy_notifyer.env import Env


def get_telegram_creds() -> Union[Tuple[str, int], Tuple[str, List[int]]]:
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
    if len(chat_id) == 1:
        return token, chat_id[0]
    return token, chat_id


async def run_sync(func: Callable, *args, **kwargs):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

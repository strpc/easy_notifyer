import os
from datetime import datetime
from socket import gethostname
from typing import Tuple, Optional, List, Union


DATE_FORMAT = os.getenv('EASY_NOTIFYER_DATE_FORMAT', '%Y-%m-%d %H:%M:%S')
PROJECT_NAME = os.getenv('EASY_NOTIFYER_PROJECT_NAME')


def make_report(tback: str, func_name: Optional[str] = None) -> str:
    crash_time = datetime.now().replace(microsecond=0)
    host_name = gethostname()
    report = [
        "Your program has crashed ☠️",
        'Machine name: %s' % host_name,
        'Crash date: %s' % crash_time.strftime(DATE_FORMAT),
        "Traceback:",
        '%s' % tback
    ]
    if PROJECT_NAME is not None:
        report.insert(1, 'Project: %s' % PROJECT_NAME)
    if func_name is not None:
        report.insert(3, 'Main call: %s' % func_name)
    text = '\n'.join(report)
    return text


def get_telegram_creds() -> Union[Tuple[str, int], Tuple[str, List[int]]]:
    token = os.getenv('EASY_NOTIFYER_BOT_TOKEN')
    chat_id = os.getenv('EASY_NOTIFYER_CHAT_ID')
    error = EnvironmentError(f"Telegram token or chat_id is not found. token={token}, "
                             f"chat_id={chat_id}")
    if token is None or chat_id is None:
        raise error
    try:
        chat_id = [i.strip() for i in chat_id.split(',')]
        chat_id = [int(i) for i in chat_id if i]
    except ValueError:
        raise error
    if len(chat_id) == 1:
        return token, chat_id[0]
    return token, chat_id

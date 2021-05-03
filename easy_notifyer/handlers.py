import asyncio
import functools
import traceback
from typing import List, Optional, Tuple, Type, Union

from easy_notifyer.config import get_config
from easy_notifyer.mailer import Mailer
from easy_notifyer.report import Report
from easy_notifyer.telegram import Telegram, TelegramAsync
from easy_notifyer.utils import generate_filename, run_in_threadpool


def telegram_reporter(
    *,
    token: Optional[str] = None,
    chat_id: Optional[Union[List[int], int]] = None,
    api_url: Optional[str] = None,
    exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException],
                                                          ...]]] = None,
    header: Optional[str] = None,
    as_attached: bool = False,
    **params,
):
    """
    Handler errors for sending report in telegram.
    Args:
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
            variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        api_url(str): #! TODO
        exceptions(exception, tuple(exception), optional): Exceptions for handle. Two and more - in
            tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.
        **params:
            filename(str, optional): filename for sending report as file.
                Default: datetime %Y-%m-%d %H_%M_%S.txt. Format may be set in environment variable
                EASY_NOTIFYER_FILENAME_DT_FORMAT
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
                as_attached report.
    """
    exceptions = exceptions or Exception

    def decorator(func):
        func_name = func.__name__

        def sync_wrapped_view(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                tback = traceback.format_exc()
                report = _report_maker(
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                _report_telegram_handler(report=report,
                                         token=token,
                                         chat_id=chat_id,
                                         api_url=api_url,
                                         **params)
                raise exc

        async def async_wrapped_view(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                tback = traceback.format_exc()
                report = await run_in_threadpool(
                    _report_maker,
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                await _async_report_telegram_handler(report=report,
                                                     token=token,
                                                     chat_id=chat_id,
                                                     api_url=api_url,
                                                     **params)
                raise exc

        if asyncio.iscoroutinefunction(func):
            return functools.wraps(func)(async_wrapped_view)
        return functools.wraps(func)(sync_wrapped_view)

    return decorator


def _report_maker(
    *,
    tback: str,
    func_name: Optional[str] = None,
    header: Optional[str] = None,
    as_attached: bool = False,
) -> Report:
    """
    Make report from
    Args:
        tback(str): traceback for report.
        func_name(str, optional): name of function when raised error.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.
    Returns:
        isinstance of Report obj.
    """
    return Report(tback, func_name, header, as_attached)


def _report_telegram_handler(
    *,
    report: Report,
    token: Optional[str] = None,
    chat_id: Optional[Union[int, List[int]]] = None,
    api_url: Optional[str] = None,
    **kwargs,
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
            variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): make report for sending as a file.
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
                as_attached report.
    """
    config = get_config()
    token = token or config.telegram.token
    chat_id = chat_id or config.telegram.chat_id
    api_url = api_url or config.telegram.api_url
    bot = Telegram(token=token, chat_id=chat_id, api_url=api_url)
    if report.attach is not None:
        filename = kwargs.pop("filename", None) or generate_filename(
            config.report.filename_dt_format)
        bot.send_attach(msg=report.report,
                        attach=report.attach,
                        filename=filename,
                        **kwargs)
    else:
        bot.send_message(report.report, **kwargs)


async def _async_report_telegram_handler(
    *,
    report: Report,
    token: Optional[str] = None,
    chat_id: Optional[Union[int, List[int]]] = None,
    api_url: Optional[str] = None,
    **kwargs,
):
    """
    Send report.
    Args:
        report(Report): instance of ready to send report.
        token(str, optional): Telegram bot token. Can be use from environment variable
            `EASY_NOTIFYER_TELEGRAM_TOKEN`. To receive: https://core.telegram.org/bots#6-botfather.
        chat_id(int, list, optional): Chat ids for send message. Can be use from environment
            variable `EASY_NOTIFYER_TELEGRAM_CHAT_ID`.
        **kwargs:
            filename(str, optional): filename for sending report as file.
                Default: datetime %Y-%m-%d %H_%M_%S.txt. Format may be set in environment variable
                EASY_NOTIFYER_FILENAME_DT_FORMAT
            disable_notification(bool): True to disable notification of message.
            disable_web_page_preview(bool): True to disable web preview for links. Not worked for
                as_attached report.
    """
    config = get_config()
    token = token or config.telegram.token
    chat_id = chat_id or config.telegram.chat_id
    api_url = api_url or config.telegram.api_url

    bot = TelegramAsync(token=token, chat_id=chat_id, api_url=api_url)
    if report.attach is not None:
        filename = kwargs.pop("filename") or generate_filename(
            config.report.filename_dt_format)
        await bot.send_attach(msg=report.report,
                              attach=report.attach,
                              filename=filename,
                              **kwargs)
    else:
        await bot.send_message(report.report, **kwargs)


def _report_mailer_handler(*, report: Report, **params):
    config = get_config()
    to_send = {
        "filename":
        params.pop("filename",
                   generate_filename(config.report.filename_dt_format)),
        "attach":
        report.attach,
        "from_addr":
        params.pop("from_addr"),
        "to_addrs":
        params.pop("to_addrs"),
        "subject":
        params.pop("subject"),
    }
    with Mailer(**params) as mailer:
        mailer.send_message(message=report.report, **to_send)


def mailer_reporter(
    *,
    exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException],
                                                          ...]]] = None,
    header: Optional[str] = None,
    as_attached: bool = False,
    **params,
):
    """
    Handler errors for sending report on email.
    Args:
        exceptions(exception, tuple(exception), optional): Exceptions for handle.
            Two and more - in tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.
        **params:
            host(str, optional): = post of smtp server. Can be use from environment variable -
                EASY_NOTIFYER_MAILER_HOST
            port(int, optional): = port of smtp server. Can be use from environment variable -
                EASY_NOTIFYER_MAILER_PORT
            login(str, optional): = login for auth in smtp server. Can be use from environment
                variable -  EASY_NOTIFYER_MAILER_LOGIN
            password(str, optional): password for auth in smtp server. Can be use from environment
                variable - EASY_NOTIFYER_MAILER_PASSWORD
            ssl(bool, optional): use SSL connection for smtp. Can be use from environment variable -
                EASY_NOTIFYER_MAILER_SSL
            from_addr(str, optional): the address sending this mail. Can be use from environment
                variable - EASY_NOTIFYER_MAILER_FROM
            to_addrs(str, list(str), optional): addresses to send this mail to. Can be use from
                environment variable - EASY_NOTIFYER_MAILER_TO
            subject(str, optional): subject of the mail.
            filename(str, optional): filename for sending report as file.
                Default: datetime %Y-%m-%d %H_%M_%S.txt. Format may be set in environment variable
                EASY_NOTIFYER_FILENAME_DT_FORMAT
    """
    exceptions = exceptions or Exception

    def decorator(func):
        func_name = func.__name__

        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except exceptions as exc:
                tback = traceback.format_exc()
                report = await run_in_threadpool(
                    _report_maker,
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                await run_in_threadpool(_report_mailer_handler,
                                        report=report,
                                        **params)
                raise exc

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                tback = traceback.format_exc()
                report = _report_maker(
                    tback=tback,
                    func_name=func_name,
                    header=header,
                    as_attached=as_attached,
                )
                _report_mailer_handler(report=report, **params)
                raise exc

        if asyncio.iscoroutinefunction(func) is True:
            return functools.wraps(func)(async_wrapper)
        return functools.wraps(func)(wrapper)

    return decorator

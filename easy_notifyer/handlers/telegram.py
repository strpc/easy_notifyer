import asyncio
import functools
import logging
import traceback
from typing import Callable, List, Optional, Tuple, Type, Union

from easy_notifyer.clients.telegram import Telegram, TelegramAsync
from easy_notifyer.report import Report
from easy_notifyer.utils import generate_filename, run_in_threadpool


logger = logging.getLogger(__name__)


def _report_maker(
    *,
    tback: str,
    func_name: Optional[str],
    header: Optional[str],
    as_attached: bool,
    service_name: Optional[str],
    datetime_format: str,
) -> Report:
    """Make report from.

    Args:
        tback (str): traceback for report.
        func_name (str, optional): name of function when raised error.
        header (str, optional): first line in report message. Default -
        "Your program has crashed ☠️"
        as_attached (bool, optional): make report for sending as a file. Default - False.
        service_name (optional): Service name.
        datetime_format (str, optional): format datetime for report.

    Returns:
        isinstance of Report obj.
    """
    return Report(tback, func_name, header, as_attached, service_name, datetime_format)


def _report_telegram_handler(
    *,
    report: Report,
    token: str,
    chat_id: Union[int, List[int]],
    api_url: Optional[str],
    filename: Optional[str],
    disable_notification: bool,
    disable_web_page_preview: bool,
):
    """Send report.

    Args:
        report (Report): instance of ready to send report.
        token (str): Telegram bot token.
        chat_id (int, list): Chat ids for send message.
        filename (str, optional): make report for sending as a file.
        disable_notification (bool): True to disable notification of message.
        disable_web_page_preview (bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = Telegram(token=token, chat_id=chat_id, api_url=api_url)
    if report.attach is not None:
        filename = filename or generate_filename()
        bot.send_attach(
            msg=report.report,
            attach=report.attach,
            filename=filename,
            disable_notification=disable_notification,
        )
    else:
        bot.send_message(
            report.report,
            disable_notification=disable_notification,
            disable_web_page_preview=disable_web_page_preview,
        )


async def _async_report_telegram_handler(
    *,
    report: Report,
    token: str,
    chat_id: Union[int, List[int]],
    api_url: Optional[str],
    filename: Optional[str],
    disable_notification: bool,
    disable_web_page_preview: bool,
):
    """Send report.

    Args:
        report (Report): instance of ready to send report.
        token (str): Telegram bot token.
        chat_id (int, list): Chat ids for send message.
        filename (str, optional): make report for sending as a file.
        disable_notification (bool): True to disable notification of message.
        disable_web_page_preview (bool): True to disable web preview for links. Not worked for
            as_attached report.
    """
    bot = TelegramAsync(token=token, chat_id=chat_id, api_url=api_url)
    if report.attach is not None:
        filename = filename or generate_filename()
        await bot.send_attach(
            msg=report.report,
            attach=report.attach,
            filename=filename,
            disable_notification=disable_notification,
        )
    else:
        await bot.send_message(
            report.report,
            disable_notification=disable_notification,
            disable_web_page_preview=disable_web_page_preview,
        )


def telegram_reporter(
    *,
    token: str,
    chat_id: Union[List[int], List[str], int, str],
    api_url: Optional[str] = None,
    service_name: Optional[str] = None,
) -> Union[Callable]:
    """Handler errors for sending report in telegram.

    Args:
        token (str): Telegram bot token. Can be use from environment variable
        To receive: https://core.telegram.org/bots#6-botfather.
        chat_id (int, str, list): Chat ids for send message.
        api_url (str): Url api for telegram.
        service_name (optional): Service name.
    """

    def telegram_wrapper(
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        datetime_format: str = "%Y-%m-%d %H:%M:%S",
        filename: Optional[str] = None,
        disable_notification: bool = False,
        disable_web_page_preview: bool = False,
    ):
        """Handler errors for sending report in telegram.
        Args:
            exceptions (exception, tuple(exception), optional): Exceptions for handle.
                Two and more - in tuple. Default - Exception.
            header (str, optional): first line in report message.
                Default - "Your program has crashed ☠️"
            as_attached (bool, optional): make report for sending as a file. Default - False.
            datetime_format (str, optional): format datetime for report.
            filename (str, optional): filename for sending report as file.
                Default: datetime %Y-%m-%d %H_%M_%S.txt.
            disable_notification (bool): True to disable notification of message.
            disable_web_page_preview (bool): True to disable web preview for links.
                Not worked for as_attached report.
        """
        if as_attached is True and disable_web_page_preview is True:
            logger.error(
                "Argument disable_web_page_preview not may be True if report mode as_attached"
            )
            disable_web_page_preview = False

        exceptions = exceptions or Exception
        datetime_format = datetime_format

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
                        service_name=service_name,
                        datetime_format=datetime_format,
                    )
                    _report_telegram_handler(
                        report=report,
                        token=token,
                        chat_id=chat_id,
                        api_url=api_url,
                        filename=filename,
                        disable_notification=disable_notification,
                        disable_web_page_preview=disable_web_page_preview,
                    )
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
                        service_name=service_name,
                        datetime_format=datetime_format,
                    )
                    await _async_report_telegram_handler(
                        report=report,
                        token=token,
                        chat_id=chat_id,
                        api_url=api_url,
                        filename=filename,
                        disable_notification=disable_notification,
                        disable_web_page_preview=disable_web_page_preview,
                    )
                    raise exc

            if asyncio.iscoroutinefunction(func):
                return functools.wraps(func)(async_wrapped_view)
            return functools.wraps(func)(sync_wrapped_view)

        return decorator

    return telegram_wrapper

import asyncio
import functools
import traceback
from typing import Optional, Tuple, Type, Union

from easy_notifyer.clients.mailer import Mailer
from easy_notifyer.report import Report
from easy_notifyer.utils import generate_filename, run_in_threadpool


def _report_mailer_handler(*, report: Report, **params):
    to_send = {
        "filename": params.pop("filename", generate_filename()),
        "attach": report.attach,
        "from_addr": params.pop("from_addr"),
        "to_addrs": params.pop("to_addrs"),
        "subject": params.pop("subject"),
    }
    with Mailer(**params) as mailer:
        mailer.send_message(message=report.report, **to_send)


def mailer_reporter(
    *,
    exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
    header: Optional[str] = None,
    as_attached: bool = False,
    **params,
):
    """Handler errors for sending report on email.

    Args:
        exceptions(exception, tuple(exception), optional): Exceptions for handle.
            Two and more - in tuple. Default - Exception.
        header(str, optional): first line in report message. Default - "Your program has crashed ☠️"
        as_attached(bool, optional): make report for sending as a file. Default - False.

        **params:
            host(str, optional): = post of smtp server.
            port(int, optional): = port of smtp server.
            login(str, optional): = login for auth in smtp server.
            password(str, optional): password for auth in smtp server.
            ssl(bool, optional): use SSL connection for smtp.
            from_addr(str, optional): the address sending this mail.
            to_addrs(str, list(str), optional): addresses to send this mail to.
            subject(str, optional): subject of the mail.
            filename(str, optional): filename for sending report as file.
            Default: datetime %Y-%m-%d %H_%M_%S.txt.
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
                await run_in_threadpool(_report_mailer_handler, report=report, **params)
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

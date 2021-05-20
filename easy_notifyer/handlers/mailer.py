import asyncio
import functools
import traceback
from typing import Callable, List, Optional, Tuple, Type, Union

from easy_notifyer.clients.mailer import Mailer
from easy_notifyer.report import Report
from easy_notifyer.utils import generate_filename, run_in_threadpool


def _report_mailer_handler(
    *,
    report: Report,
    host: str,
    port: int,
    login: str,
    password: str,
    from_addr: str,
    to_addrs: Union[str, List[str]],
    ssl: bool = False,
    filename: Optional[str] = None,
    subject: Optional[str] = None,
):
    with Mailer(
        host=host,
        port=port,
        login=login,
        password=password,
        ssl=ssl,
    ) as mailer:
        mailer.send_message(
            message=report.report,
            from_addr=from_addr,
            to_addrs=to_addrs,
            subject=subject,
            attach=report.attach,
            filename=filename or generate_filename(),
        )


def mailer_reporter(
    *,
    host: str,
    port: int,
    login: str,
    password: str,
    from_addr: str,
    to_addrs: Union[str, List[str]],
    ssl: bool = False,
    service_name: Optional[str] = None,
) -> Callable:
    """Handler errors for sending report on email.

    Args:
        host(str, optional): = post of smtp server.
        port(int, optional): = port of smtp server.
        login(str, optional): = login for auth in smtp server.
        password(str, optional): password for auth in smtp server.
        from_addr(str, optional): the address sending this mail.
        to_addrs(str, list(str), optional): addresses to send this mail to.
        ssl(bool, optional): use SSL connection for smtp.
        service_name (optional): Service name.
    """

    def mailer_wrapper(
        *,
        exceptions: Optional[Union[Type[BaseException], Tuple[Type[BaseException], ...]]] = None,
        header: Optional[str] = None,
        as_attached: bool = False,
        datetime_format: str = "%Y-%m-%d %H:%M:%S",
        subject: Optional[str] = None,
        filename: Optional[str] = None,
    ):
        """Handler errors for sending report on email.

        Args:
            exceptions (exception, tuple(exception), optional): Exceptions for handle.
                Two and more - in tuple. Default - Exception.
            header (str, optional): first line in report message. Default -
            "Your program has crashed ☠️"
            as_attached (bool, optional): make report for sending as a file. Default - False.
            datetime_format (str, optional): format datetime for report.
            subject(str, optional): subject of the mail.
            filename(str, optional): filename for sending report as file.
                Default: datetime %Y-%m-%d %H_%M_%S.txt.
        """
        exceptions = exceptions or Exception
        params_for_send = {
            "host": host,
            "port": port,
            "login": login,
            "password": password,
            "from_addr": from_addr,
            "to_addrs": to_addrs,
            "ssl": ssl,
            "filename": filename,
            "subject": subject,
        }

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
                        service_name=service_name,
                        datetime_format=datetime_format,
                    )
                    await run_in_threadpool(
                        _report_mailer_handler,
                        report=report,
                        **params_for_send,
                    )
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
                        service_name=service_name,
                        datetime_format=datetime_format,
                    )
                    _report_mailer_handler(report=report, **params_for_send)
                    raise exc

            if asyncio.iscoroutinefunction(func) is True:
                return functools.wraps(func)(async_wrapper)
            return functools.wraps(func)(wrapper)

        return decorator

    return mailer_wrapper


def _report_maker(
    *,
    tback: str,
    func_name: Optional[str] = None,
    header: Optional[str] = None,
    as_attached: bool = False,
    service_name: Optional[str],
    datetime_format: Optional[str],
) -> Report:
    """
    Make report from
    Args:
        tback (str): traceback for report.
        func_name (str, optional): name of function when raised error.
        header (str, optional): first line in report message. Default -
        "Your program has crashed ☠️"
        as_attached (bool, optional): make report for sending as a file. Default - False.
    Returns:
        isinstance of Report obj.
    """
    return Report(tback, func_name, header, as_attached, service_name, datetime_format)

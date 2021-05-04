# pylint: disable=too-few-public-methods, too-many-instance-attributes
from datetime import datetime
from socket import gethostname
from typing import Optional


class Report:
    """Object for create report"""

    def __init__(
        self,
        tback: str,
        func_name: Optional[str],
        header: Optional[str],
        as_attached: bool,
        service_name: Optional[str],
        datetime_format: Optional[str],
    ):
        self._tback = tback
        self._func_name = func_name
        self._header = header
        self._host_name = gethostname()
        self._service_name = service_name
        self._as_attached = as_attached
        self._datetime_format = datetime_format
        self.report = None
        self.attach = None
        if self._as_attached is True:
            self._make_attach_report()
        else:
            self._make_text_report()

    def _make_text_report(self):
        """Formatting text report before sending."""
        crash_time = datetime.now().replace(microsecond=0)
        report = [
            "Your program has crashed ☠️",
            "Machine name: %s" % self._host_name,
            "Crash date: %s" % crash_time.strftime(self._datetime_format),
            "Traceback:",
            "%s" % self._tback,
        ]
        if self._header is not None:
            report[0] = "%s" % self._header
        if self._service_name is not None:
            report.insert(1, "Service: %s" % self._service_name)
        if self._func_name is not None:
            report.insert(3, "Main call: %s" % self._func_name)
        self.report = "\n".join(report)

    def _make_attach_report(self):
        """Formatting report with attach before sending."""
        crash_time = datetime.now().replace(microsecond=0)
        report = [
            "Your program has crashed ☠️",
            "Machine name: %s" % self._host_name,
            "Crash date: %s" % crash_time.strftime(self._datetime_format),
        ]
        if self._header is not None:
            report.insert(0, "%s" % self._header)
        if self._service_name is not None:
            report.insert(1, "Service: %s" % self._service_name)
        if self._func_name is not None:
            report.insert(2, "Main call: %s" % self._func_name)
        self.report = "\n".join(report)
        self.attach = self._tback

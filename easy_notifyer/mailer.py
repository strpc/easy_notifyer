import uuid
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from typing import BinaryIO, List, Optional, Union

from easy_notifyer.env import Env
from easy_notifyer.exceptions import ConfigError


class Mailer:
    """Object for send mail"""

    def __init__(
        self,
        *,
        host: Optional[str] = None,
        port: Optional[int] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        ssl: Optional[bool] = None,
    ):
        """
        Args:
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
        """
        env = Env()
        self._host = host or env.EASY_NOTIFYER_MAILER_HOST
        self._port = port or env.EASY_NOTIFYER_MAILER_PORT
        self._login = login or env.EASY_NOTIFYER_MAILER_LOGIN
        self._password = password or env.EASY_NOTIFYER_MAILER_PASSWORD
        self._ssl = ssl or env.EASY_NOTIFYER_MAILER_SSL
        self._connection: Optional[SMTP_SSL, SMTP] = None

        if not all([self._host, self._port]):
            raise ConfigError(host=self._host, port=self._port)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()

    def connect(self):
        """Connect to smtp-server and create session"""
        if self._connection is None:
            type_conn = SMTP_SSL if self._ssl is True else SMTP
            self._connection = type_conn(host=self._host, port=self._port)
        self.login()

    def login(self):
        """Create session with login/password"""
        if self._connection is not None and self._login is not None and self._password is not None:
            self._connection.login(user=self._login, password=self._password)

    def disconnect(self):
        """Terminate session"""
        if self._connection is not None:
            self._connection.quit()

    @staticmethod
    def _format_message(
        *,
        from_addr: str,
        to_addrs: List[str],
        text: str,
        subject: Optional[str] = None,
        attach: Optional[Union[bytes, str, BinaryIO]] = None,
        filename: Optional[str] = None,
    ) -> MIMEMultipart:
        """
        Formatting message for send.
        Args:
            from_addr(str): the address sending this mail.
            to_addrs(list(str)): addresses to send this mail to.
            subject(str, optional): subject of the mail.
            attach(bytes, str, tuple, optional): file to send.
            filename(str, optional): filename for attached file.
        Returns:
            MIMEMultipart of message with body, from, to, attach and subject.
        """
        message = MIMEMultipart()
        message["From"] = from_addr
        message["To"] = ", ".join(to_addrs)
        message["Subject"] = subject
        message.attach(MIMEText(text))

        if attach is not None:
            filename = filename or uuid.uuid4().hex
            if hasattr(attach, "read") and isinstance(attach.read(0), bytes):
                attach = attach.read()
            elif hasattr(attach, "encode"):
                attach = attach.encode()
            message.attach(MIMEApplication(attach, name=filename))
        return message

    def send_message(
        self,
        *,
        message: Optional[str] = None,
        from_addr: Optional[str] = None,
        to_addrs: Optional[Union[str, List[str]]] = None,
        subject: Optional[str] = None,
        attach: Optional[Union[bytes, str, BinaryIO]] = None,
        filename: Optional[str] = None,
    ):
        """
        Send email.
        Args:
            message(str, optional): Text body of message.
            from_addr(str, optional): the address sending this mail. Can be use from environment
                variable - EASY_NOTIFYER_MAILER_FROM
            to_addrs(str, list(str), optional): addresses to send this mail to. Can be use from
                environment variable - EASY_NOTIFYER_MAILER_TO
            subject(str, optional): subject of the mail.
            attach(bytes, str, tuple, optional): file to send.
            filename(str, optional): filename for attached file.
        """
        from_addr = from_addr or Env().EASY_NOTIFYER_MAILER_FROM
        to_addrs = to_addrs or Env().EASY_NOTIFYER_MAILER_TO
        if from_addr is None or to_addrs is None:
            raise EnvironmentError(
                f"from_addr or to_addrs is uncorrect. from_addr={from_addr}" f"to_addrts={to_addrs}"
            )

        to_addrs = [mail.strip() for mail in to_addrs.split(",")]
        msg = self._format_message(
            from_addr=from_addr,
            to_addrs=to_addrs,
            text=message,
            subject=subject,
            attach=attach,
            filename=filename,
        )

        self._connection.sendmail(from_addr=from_addr, to_addrs=to_addrs, msg=msg.as_string())

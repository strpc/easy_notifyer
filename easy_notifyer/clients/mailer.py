import uuid
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL
from typing import BinaryIO, List, Optional, Union


class Mailer:
    """Object for send mail"""

    def __init__(
        self,
        *,
        host: str,
        port: int,
        login: str,
        password: str,
        ssl: bool = False,
    ):
        """
        Args:
            host (str, optional): = post of smtp server.
            port (int, optional): = port of smtp server.
            login (str, optional): = login for auth in smtp server.
            password (str, optional): password for auth in smtp server.
            ssl (bool, optional): use SSL connection for smtp.
        """
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self._ssl = ssl
        self._connection: Optional[SMTP_SSL, SMTP] = None

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
        subject: str,
        attach: Union[bytes, str, BinaryIO],
        filename: str,
    ) -> MIMEMultipart:
        """Formatting message for send.

        Args:
            from_addr (str): the address sending this mail.
            to_addrs (list(str)): addresses to send this mail to.
            subject (str, optional): subject of the mail.
            attach (bytes, str, tuple, optional): file to send.
            filename (str, optional): filename for attached file.

        Returns:
            MIMEMultipart: multipart of message with body, from, to, attach and subject.
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
        from_addr: str,
        to_addrs: Union[str, List[str]],
        subject: Optional[str] = None,
        attach: Optional[Union[bytes, str, BinaryIO]] = None,
        filename: Optional[str] = None,
    ):
        """Send email.

        Args:
            message (str, optional): Text body of message.
            from_addr (str, optional): the address sending this mail.
            to_addrs (str, list(str), optional): addresses to send this mail to.
            subject (str, optional): subject of the mail.
            attach (bytes, str, tuple, optional): file to send.
            filename (str, optional): filename for attached file.
        """
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

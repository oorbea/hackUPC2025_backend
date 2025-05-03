import smtplib
from typing import List, Optional, Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailSender:
    """
    Configurable email sender supporting plain-text and HTML content.
    """
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int = 587,
        username: Optional[str] = None,
        password: Optional[str] = None,
        use_tls: bool = True,
        use_ssl: bool = False,
        default_from: Optional[str] = None,
        timeout: int = 10
    ):
        """
        :param smtp_server: SMTP host (e.g. "smtp.gmail.com")
        :param smtp_port: port number (usually 587 for TLS, 465 for SSL)
        :param username: SMTP username (if authentication is required)
        :param password: SMTP password
        :param use_tls: whether to initiate STARTTLS
        :param use_ssl: whether to use SMTP_SSL
        :param default_from: default "From" address (falls back to username)
        :param timeout: socket timeout in seconds
        """
        self.server = smtp_server
        self.port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        self.use_ssl = use_ssl
        self.default_from = default_from or username
        self.timeout = timeout

    def send_email(
        self,
        subject: str,
        to: Union[str, List[str]],
        body_text: Optional[str] = None,
        body_html: Optional[str] = None,
        cc: Optional[Union[str, List[str]]] = None,
        bcc: Optional[Union[str, List[str]]] = None,
    ):
        """
        Send an email.

        :param subject: email subject
        :param to: recipient or list of recipients
        :param body_text: plain-text version of the message
        :param body_html: HTML version of the message
        :param cc: CC recipient or list
        :param bcc: BCC recipient or list
        """

        to_list  = [to]  if isinstance(to, str)  else list(to or [])
        cc_list  = [cc]  if isinstance(cc, str)  else list(cc or [])
        bcc_list = [bcc] if isinstance(bcc, str) else list(bcc or [])

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From']    = self.default_from
        msg['To']      = ', '.join(to_list)
        if cc_list:
            msg['Cc'] = ', '.join(cc_list)

        if body_text:
            msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
        if body_html:
            msg.attach(MIMEText(body_html, 'html',  'utf-8'))

        all_recipients = to_list + cc_list + bcc_list

        if self.use_ssl:
            smtp = smtplib.SMTP_SSL(self.server, self.port, timeout=self.timeout)
        else:
            smtp = smtplib.SMTP(self.server, self.port, timeout=self.timeout)

        try:
            smtp.ehlo()
            if self.use_tls and not self.use_ssl:
                smtp.starttls()
                smtp.ehlo()

            if self.username and self.password:
                smtp.login(self.username, self.password)

            smtp.sendmail(self.default_from, all_recipients, msg.as_string())
        finally:
            smtp.quit()

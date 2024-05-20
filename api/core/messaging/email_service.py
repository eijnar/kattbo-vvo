import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template as JinjaTemplate
from core.messaging.base import MessagingService
from core.messaging.template_service import TemplateService
import logging
from email.header import Header
from email.utils import formataddr

logger = logging.getLogger(__name__)

class EmailService(MessagingService):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, template_service: TemplateService):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.template_service = template_service

    async def send_message(self, recipient: str, subject: str, message: str) -> None:
        sender_email = "info@kaffesump.se"
        sender_name = "Kättbo Viltvårdsområde"
        msg = MIMEMultipart()
        msg['From'] = formataddr((str(Header(sender_name, 'utf-8')), sender_email))
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        logger.debug((f"Email from: {msg['From']}"))
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, recipient, msg.as_string())

    async def set_template(self, template_name: str, context: dict) -> str:
        template = await self.template_service.get_template(
            service='email', name=template_name)
        if not template:
            raise ValueError(
                f"Template {template_name} not found for email service")
        subject_template = JinjaTemplate(template.subject)
        content_template = JinjaTemplate(template.content)
        return subject_template.render(context), content_template.render(context)

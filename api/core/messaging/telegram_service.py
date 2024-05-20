import httpx
from jinja2 import Template as JinjaTemplate

from core.messaging.factory import MessagingService
from core.messaging.template_service import TemplateService


class TelegramService(MessagingService):
    def __init__(self, bot_token: str, template_service: TemplateService):
        self.bot_token = bot_token
        self.template_service = template_service

    async def send_message(self, recipient: str, subject: str, message: str) -> None:
        full_message = f"{subject}\n{message}"
        async with httpx.AsyncClient() as client:
            await client.post(
                f'https://api.telegram.org/bot{self.bot_token}/sendMessage',
                json={'chat_id': recipient, 'text': full_message}
            )

    async def set_template(self, template_name: str, context: dict) -> str:
        template = await self.template_service.get_template(service='telegram', name=template_name)
        if not template:
            raise ValueError(
                f"Template {template_name} not found for telegram service")
        content_template = JinjaTemplate(template.content)
        return "", content_template.render(context)

from abc import ABC, abstractmethod
from typing import Tuple

class MessagingService(ABC):
    @abstractmethod
    async def send_message(self, recipient: str, subject: str, message: str) -> None:
        pass

    @abstractmethod
    def set_template(self, template_name: str, context: dict) -> Tuple[str, str]:
        pass

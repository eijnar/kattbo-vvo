from typing import Dict

from core.messaging.base import MessagingService


class MessagingServiceFactory:
    def __init__(self):
        self.services: Dict[str, MessagingService] = {}

    def register_service(self, service_name: str, service: MessagingService) -> None:
        self.services[service_name] = service

    def get_service(self, service_name: str) -> MessagingService:
        service = self.services.get(service_name)
        if not service:
            raise ValueError(f"Service {service_name} not found")
        return service

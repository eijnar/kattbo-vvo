import logging
from fastapi import APIRouter, HTTPException
from core.messaging.tasks import send_notification_task
notification = APIRouter()
logger = logging.getLogger(__name__)

@notification.post("/send-notification/")
async def send_notification(
    service_name: str,
    recipient: str,
    template_name: str,
    context: dict
):
    try:
        send_notification_task.delay(service_name, recipient, template_name, context)
        return {"status": "Notification task queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
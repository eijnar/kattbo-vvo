import logging
from fastapi import APIRouter, HTTPException
from schemas.notification import NotificationRequest
from core.tasks.notification_task import send_notification_task


router = APIRouter(tags=["notification"])
logger = logging.getLogger("tjolaop")


@router.post("/send-notification/")
async def send_notification(notification: NotificationRequest):
    try:
        # Log the request for debugging
        logger.info(f"Sending notification: service_name={notification.service_name}, recipient={notification.recipients}, template_name={notification.template_name}, context={notification.context}")

        send_notification_task.delay(
            notification.service_name, notification.recipients, notification.template_name, notification.context.dict())
        return {"status": "Notification task queued", "job_id": "message.message_id"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


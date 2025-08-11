from celery import shared_task
from .models import NotificationRecord
from .services import NotificationService


@shared_task(bind=True, max_retries=3)
def send_notification_task(self, record_id: int):
    service = NotificationService()
    record = NotificationRecord.objects.get(id=record_id)
    service.send(record)

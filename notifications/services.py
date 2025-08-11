import logging
from django.conf import settings
from django.core.mail import EmailMessage
from .models import NotificationRecord, Channel, DeviceToken

try:
    from firebase_admin import messaging, credentials, initialize_app
    if settings.FCM_CREDENTIALS:
        initialize_app(credentials.Certificate(settings.FCM_CREDENTIALS))
except Exception:  # pragma: no cover - firebase optional
    messaging = None

logger = logging.getLogger(__name__)


class EmailChannel:
    def send(self, record: NotificationRecord):
        context = record.context or {}
        subject = record.subject
        message = record.message
        if record.template:
            subject = subject or record.template.subject.format(**context)
            message = message or record.template.content.format(**context)
        email = EmailMessage(subject, message, to=[record.recipient.email])
        for attachment in record.attachments.all():
            email.attach_file(attachment.file.path)
        email.send()


class SMSChannel:
    def send(self, record: NotificationRecord):
        logger.info('SMS to %s: %s', record.recipient, record.message)


class PushChannel:
    def send(self, record: NotificationRecord):
        if not messaging:
            raise RuntimeError('firebase-admin not configured')
        tokens = DeviceToken.objects.filter(user=record.recipient).values_list('token', flat=True)
        if not tokens:
            raise RuntimeError('No device tokens')
        msg = messaging.MulticastMessage(
            notification=messaging.Notification(title=record.subject, body=record.message),
            tokens=list(tokens),
        )
        messaging.send_multicast(msg)


class NotificationService:
    CHANNEL_MAP = {
        Channel.EMAIL: EmailChannel(),
        Channel.SMS: SMSChannel(),
        Channel.PUSH: PushChannel(),
    }

    def send(self, record: NotificationRecord):
        handler = self.CHANNEL_MAP.get(record.channel)
        if not handler:
            raise ValueError(f'Unsupported channel {record.channel}')
        try:
            handler.send(record)
            record.status = 'sent'
        except Exception as exc:
            record.status = 'failed'
            record.error = str(exc)
            logger.exception('Failed to send notification %s', record.id)
            if record.channel == Channel.PUSH and record.recipient and record.recipient.email:
                fallback = NotificationRecord.objects.create(
                    template=record.template,
                    recipient=record.recipient,
                    channel=Channel.EMAIL,
                    subject=record.subject,
                    message=record.message,
                    context=record.context,
                )
                self.send(fallback)
        finally:
            record.save()

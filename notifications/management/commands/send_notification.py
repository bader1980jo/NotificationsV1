from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notifications.models import NotificationTemplate, NotificationRecord
from notifications.services import NotificationService

User = get_user_model()


class Command(BaseCommand):
    help = 'Send a notification to a user'

    def add_arguments(self, parser):
        parser.add_argument('template_id', type=int)
        parser.add_argument('user_id', type=int)

    def handle(self, template_id, user_id, **options):
        template = NotificationTemplate.objects.get(pk=template_id)
        user = User.objects.get(pk=user_id)
        record = NotificationRecord.objects.create(
            template=template,
            recipient=user,
            channel=template.channel,
            subject=template.subject,
            message=template.content,
        )
        NotificationService().send(record)
        self.stdout.write(self.style.SUCCESS('Notification sent'))

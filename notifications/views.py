from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import NotificationTemplate, NotificationRecord, DeviceToken, Attachment
from .serializers import (
    NotificationTemplateSerializer,
    NotificationRecordSerializer,
    DeviceTokenSerializer,
    NotificationSendSerializer,
    AttachmentSerializer,
)
from .tasks import send_notification_task

User = get_user_model()


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NotificationRecord.objects.all().order_by('-created_at')
    serializer_class = NotificationRecordSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def send(self, request):
        serializer = NotificationSendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        template = serializer.validated_data['template']
        user_ids = serializer.validated_data['users']
        context = serializer.validated_data.get('context', {})
        attachments = serializer.validated_data.get('attachments', [])
        users = User.objects.filter(id__in=user_ids)
        for user in users:
            record = NotificationRecord.objects.create(
                template=template,
                recipient=user,
                channel=template.channel,
                context=context,
                subject=template.subject.format(**context),
                message=template.content.format(**context),
            )
            record.attachments.set(attachments)
            send_notification_task.delay(record.id)
        return Response({'status': 'queued'}, status=status.HTTP_202_ACCEPTED)


class NotificationTemplateViewSet(viewsets.ModelViewSet):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]


class DeviceTokenViewSet(viewsets.ModelViewSet):
    queryset = DeviceToken.objects.all()
    serializer_class = DeviceTokenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

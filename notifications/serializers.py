from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    NotificationTemplate,
    NotificationRecord,
    DeviceToken,
    Attachment,
)

User = get_user_model()


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'name', 'file']


class NotificationTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationTemplate
        fields = ['id', 'name', 'subject', 'content', 'channel']


class NotificationRecordSerializer(serializers.ModelSerializer):
    template = NotificationTemplateSerializer(read_only=True)
    recipient = serializers.StringRelatedField()

    class Meta:
        model = NotificationRecord
        fields = ['id', 'template', 'recipient', 'channel', 'status', 'message', 'created_at', 'sent_at']


class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['id', 'user', 'token', 'platform']


class NotificationSendSerializer(serializers.Serializer):
    template = serializers.PrimaryKeyRelatedField(queryset=NotificationTemplate.objects.all())
    users = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    context = serializers.DictField(required=False)
    attachments = serializers.ListField(child=serializers.PrimaryKeyRelatedField(queryset=Attachment.objects.all()), required=False)

from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Channel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push'
    IN_APP = 'in_app', 'In App'


class NotificationTemplate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    subject = models.CharField(max_length=150, blank=True)
    content = models.TextField()
    channel = models.CharField(max_length=20, choices=Channel.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or self.file.name


class DeviceToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    platform = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}:{self.platform}"


class NotificationRecord(models.Model):
    template = models.ForeignKey(NotificationTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    subject = models.CharField(max_length=150, blank=True)
    message = models.TextField(blank=True)
    context = models.JSONField(default=dict, blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
    status = models.CharField(max_length=20, default='pending')
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.channel} to {self.recipient} ({self.status})"

from django.contrib import admin
from .models import NotificationTemplate, NotificationRecord, DeviceToken, Attachment


@admin.register(NotificationTemplate)
class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'channel', 'updated_at')
    search_fields = ('name',)


@admin.register(NotificationRecord)
class NotificationRecordAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'channel', 'status', 'created_at')
    list_filter = ('channel', 'status')
    search_fields = ('recipient__username',)


@admin.register(DeviceToken)
class DeviceTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'platform')
    search_fields = ('user__username', 'token')


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'file')

from rest_framework.routers import DefaultRouter
from .views import (
    NotificationViewSet,
    NotificationTemplateViewSet,
    DeviceTokenViewSet,
    AttachmentViewSet,
)

router = DefaultRouter()
router.register('notifications', NotificationViewSet, basename='notification')
router.register('templates', NotificationTemplateViewSet, basename='template')
router.register('device-tokens', DeviceTokenViewSet, basename='device-token')
router.register('attachments', AttachmentViewSet, basename='attachment')

urlpatterns = router.urls

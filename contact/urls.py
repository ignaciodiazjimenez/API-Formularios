from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContactMessageViewSet

router = DefaultRouter()
router.register(r'contact', ContactMessageViewSet)  # Ruta para la API

urlpatterns = [
    path('', include(router.urls)),
]

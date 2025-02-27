from django.core.mail import send_mail
from rest_framework import viewsets
from decouple import config
from .models import ContactMessage
from .serializers import ContactMessageSerializer
import logging
from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    # Limitar las peticiones a 5 por minuto y bloquear si se supera por IP
    @method_decorator(ratelimit(key='ip', rate='5/m', method=['POST'], block=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def perform_create(self, serializer):
        message = serializer.save()

        # Enviar email al usuario
        try:
            send_mail(
                subject=f"Nuevo mensaje de contacto: {message.subject}",
                message=f"Hola!👋🏼 {message.name}\n He recibido tu correo desde {message.email}\n Estaré encantado de ponerme en contacto con usted lo antes posible 😎 !\n\n Un Saludo!!👋🏼",
                from_email=config('EMAIL_HOST_USER'),
                recipient_list=[message.email],
            )
            logger.info(f"Correo enviado a {message.email}")
        except Exception as e:
            logger.error(f"Error enviando correo al usuario: {str(e)}")

        # Enviar email al administrador
        try:
            send_mail(
                subject=f"Nuevo mensaje de contacto: {message.subject}",
                message=f"Atención! {message.name} nos ha mandado un correo desde {message.email}\n Correo:\n  {message.message}",
                from_email=config('EMAIL_HOST_USER'),
                recipient_list=[config('EMAIL_HOST_USER')],
            )
            logger.info("Correo enviado al administrador")
        except Exception as e:
            logger.error(f"Error enviando correo al administrador: {str(e)}")

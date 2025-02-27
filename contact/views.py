from django.core.mail import send_mail
from rest_framework import viewsets
from .models import ContactMessage
from .serializers import ContactMessageSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        message = serializer.save()

        # Enviar email cuando se recibe un mensaje nuevo
        send_mail(
            subject=f"Nuevo mensaje de contacto: {message.subject}",
            message=f"Hola!👋🏼 {message.name}\n He recibido tu correo desde {message.email}\n Estaré encantado de ponerme en contacto con usted lo antes posible 😎 !\n\n Un Saludo!!👋🏼",
            from_email="ignaciodeloyoladiazjimenez@gmail.com", 
            recipient_list=[message.email],  
            fail_silently=False,
        )
        
        # Enviar email al administrador
        send_mail(
            subject=f"Nuevo mensaje de contacto: {message.subject}",
            message=f"Atención! {message.name} nos ha mandado un correo desde {message.email}\n Correo:\n  {message.message}",
            from_email="ignaciodeloyoladiazjimenez@gmail.com", 
            recipient_list=["ignaciodeloyoladiazjimenez@gmail.com"],  
            fail_silently=False,
        )
